from flask import Blueprint, request, Response
import requests
import urllib.parse
import ssl
from requests.adapters import HTTPAdapter
from urllib3.poolmanager import PoolManager
from urllib3.util.ssl_ import create_urllib3_context

# ====================== 配置区 ======================
# 请求超时秒数
REQ_TIMEOUT = 15
# 全局跳过SSL证书校验（内网/自签证书必备）
SKIP_SSL_VERIFY = True
# ====================================================

# 创建代理蓝图
proxy_bp = Blueprint("proxy", __name__)

# 关闭SSL验证工具
class SSLAdapter(HTTPAdapter):
    def init_poolmanager(self, connections, maxsize, block=False):
        context = create_urllib3_context()
        if SKIP_SSL_VERIFY:
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
        self.poolmanager = PoolManager(
            num_pools=connections,
            maxsize=maxsize,
            block=block,
            ssl_context=context
        )

# 全局session，复用连接池
session = requests.Session()
session.mount("http://", SSLAdapter())
session.mount("https://", SSLAdapter())

# 统一跨域头
def add_cors_headers(resp: Response):
    resp.headers["Access-Control-Allow-Origin"] = "*"
    resp.headers["Access-Control-Allow-Methods"] = "GET,POST,PUT,DELETE,PATCH,OPTIONS"
    resp.headers["Access-Control-Allow-Headers"] = "*"
    resp.headers["Access-Control-Max-Age"] = "86400"
    # CSP放行本地端口，解决connect-src拦截
    csp = (
        "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; "
        "img-src 'self' data: http://localhost:* http://127.0.0.1:*; "
        "connect-src 'self' ws://localhost:* http://localhost:* http://127.0.0.1:*; "
        "font-src 'self'; object-src 'none'"
    )
    resp.headers["Content-Security-Policy"] = csp
    return resp

# 预检OPTIONS处理
@proxy_bp.route("/proxy", methods=["OPTIONS"])
def proxy_options():
    resp = Response("", status=204)
    return add_cors_headers(resp)

# 万能代理入口，支持所有常规请求方式
@proxy_bp.route("/proxy", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
def universal_proxy():
    # 1. 获取目标地址 url 参数
    target_raw = request.args.get("url", "")
    if not target_raw:
        resp = Response("缺少参数 url，示例：/proxy?url=https://xxx.com/api/data", status=400)
        return add_cors_headers(resp)
    target_url = urllib.parse.unquote(target_raw)

    # 2. 组装完整请求参数
    # 透传所有query参数（除了url本身）
    query_params = dict(request.args)
    del query_params["url"]

    # 透传headers，过滤危险头
    req_headers = {}
    skip_headers = ["host", "content-length", "content-encoding"]
    for k, v in request.headers.items():
        if k.lower() not in skip_headers:
            req_headers[k] = v
    # 默认补全浏览器UA，防止拦截
    if "user-agent" not in [h.lower() for h in req_headers.keys()]:
        req_headers["User-Agent"] = (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "Chrome/120.0.0.0 Safari/537.36"
        )

    # 3. 获取body二进制（支持文件上传、表单、json）
    body_data = request.get_data()

    try:
        # 4. 发起代理请求，流式返回
        proxy_resp = session.request(
            method=request.method,
            url=target_url,
            params=query_params,
            headers=req_headers,
            data=body_data,
            timeout=REQ_TIMEOUT,
            stream=True,  # 流式传输，大文件不占内存
            verify=not SKIP_SSL_VERIFY
        )

        # 5. 流式构建返回响应，透传状态码、content-type
        def stream_generator():
            for chunk in proxy_resp.iter_content(chunk_size=8192):
                yield chunk

        resp = Response(
            stream_generator(),
            status=proxy_resp.status_code,
            content_type=proxy_resp.headers.get("Content-Type", "text/plain")
        )

        # 透传目标服务的响应头（过滤冲突头）
        skip_res_headers = ["transfer-encoding", "connection", "content-length"]
        for k, v in proxy_resp.headers.items():
            if k.lower() not in skip_res_headers:
                resp.headers[k] = v

    except requests.exceptions.Timeout:
        resp = Response(f"请求目标 {target_url} 超时({REQ_TIMEOUT}s)", status=504)
    except requests.exceptions.ConnectionError:
        resp = Response(f"无法连接目标地址：{target_url}", status=502)
    except Exception as e:
        resp = Response(f"代理异常：{str(e)}", status=500)

    # 添加跨域+CSP头
    return add_cors_headers(resp)