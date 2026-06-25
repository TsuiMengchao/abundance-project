from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from abundance_flask.config import config  # 导入配置

# 初始化扩展（全局可用）
db = SQLAlchemy()
cors = CORS()


def create_app(env):
    """工厂函数：创建并配置Flask应用"""
    app = Flask(__name__)
    # 全局开启跨域，允许所有域名、请求头、请求方法
    CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

    # 加载对应环境的配置
    app.config.from_object(config[env])

    # 初始化扩展
    db.init_app(app)
    cors.init_app(app)

    # 注册蓝图（路由）
    from abundance_flask.app.routes.main_routes import main_bp
    app.register_blueprint(main_bp, url_prefix="/api")

    # 注册代理蓝图
    from abundance_flask.app.routes.proxy_route import proxy_bp
    app.register_blueprint(proxy_bp, url_prefix="/api")  # 代理接口路径：/api/proxy
    # 末尾添加
    from abundance_flask.app.routes.web_route import web_bp
    app.register_blueprint(web_bp)
    return app