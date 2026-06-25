from flask import Blueprint, send_from_directory, Response
import os

web_bp = Blueprint("web", __name__)
STATIC_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static")

# 静态文件后缀
static_suffix = (".js", ".css", ".png", ".jpg", ".jpeg", ".svg", ".ico",
                 ".woff", ".woff2", ".ttf", ".map", ".json", ".html")

@web_bp.route("/")
def index():
    return send_from_directory(STATIC_FOLDER, "index.html")

@web_bp.route("/<path:any_path>")
def unified_route(any_path):
    # 接口前缀直接404
    skip_prefix = ("api/", "fe-proxy/")
    for p in skip_prefix:
        if any_path.startswith(p):
            return "404 Not Found", 404

    # 判断是否为静态文件后缀
    if any_path.endswith(static_suffix):
        try:
            # 尝试读取磁盘真实文件
            return send_from_directory(STATIC_FOLDER, any_path)
        except OSError:
            # 文件不存在才404
            return "404 Not Found", 404

    # 无后缀/页面路由，全部返回SPA首页
    return send_from_directory(STATIC_FOLDER, "index.html")

@web_bp.after_request
def add_cors(resp: Response):
    resp.headers["Access-Control-Allow-Origin"] = "*"
    return resp