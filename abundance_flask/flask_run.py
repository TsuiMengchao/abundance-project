import os
import sys
import ssl
import threading
import time

from abundance_flask.app import create_app

# 根据环境变量加载配置（默认开发环境）
env = os.getenv("FLASK_ENV", "development")
app = create_app(env)

# 证书存放目录
CERT_DIR = "./ssl_cert"
CERT_FILE = os.path.join(CERT_DIR, "server.crt")
KEY_FILE = os.path.join(CERT_DIR, "server.key")

# 自动生成自签SSL证书（不存在时自动创建）
def generate_self_signed_cert():
    if os.path.exists(CERT_FILE) and os.path.exists(KEY_FILE):
        return
    os.makedirs(CERT_DIR, exist_ok=True)
    # 生成证书命令
    cmd = (
        f'openssl req -x509 -nodes -days 3650 -newkey rsa:2048 '
        f'-keyout {KEY_FILE} -out {CERT_FILE} '
        f'-subj "/C=CN/ST=Local/L=Dev/O=LocalDev/CN=127.0.0.1"'
    )
    os.system(cmd)
    print("✅ 已自动生成SSL自签证书")

# HTTPS 服务线程函数
def run_https_server():
    generate_self_signed_cert()
    # 构造SSL上下文
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ssl_context.load_cert_chain(certfile=CERT_FILE, keyfile=KEY_FILE)
    # HTTPS 端口 2115
    app.run(
        host="0.0.0.0",
        port=2115,
        debug=False,
        ssl_context=ssl_context,
        threaded=True
    )

def run_http_server():
    app.run(
        host="0.0.0.0",
        port=2114,
        debug=False,
        threaded=True
    )

class FlaskRun:
    def __init__(self):
        # # 启动HTTPS子线程
        # https_thread = threading.Thread(target=run_https_server, daemon=True)
        # https_thread.start()
        # print("🔒 HTTPS 服务已启动：https://0.0.0.0:2115")

        # 启动 HTTP 2114
        http_thread = threading.Thread(target=run_http_server, daemon=True)
        http_thread.start()
        print("🌐 HTTP 服务已启动：http://0.0.0.0:2114")


if __name__ == '__main__':
    flask_run = FlaskRun()
    while True:
        pass