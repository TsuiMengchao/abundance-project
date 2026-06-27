from flask import Flask, request, Response
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from abundance_flask.config import config

db = SQLAlchemy()

def create_app(env):
    app = Flask(__name__)

    # ========== 完整CORS配置，强制放行Content-Type ==========
    CORS(
        app,
        resources={r"/*": {"origins": "*"}},
        supports_credentials=True,
        allow_headers=["Content-Type", "Accept"],
        methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"]
    )

    app.config.from_object(config[env])
    db.init_app(app)

    # 全局兜底OPTIONS预检（核心！flask-cors偶尔失效靠这个兜底）
    @app.before_request
    def handle_preflight():
        if request.method == "OPTIONS":
            res = Response()
            res.headers["Access-Control-Allow-Origin"] = "*"
            res.headers["Access-Control-Allow-Methods"] = "GET,POST,OPTIONS"
            # 关键：明确放行Content-Type
            res.headers["Access-Control-Allow-Headers"] = "Content-Type"
            res.status_code = 204
            return res

    # 注册蓝图不变
    from abundance_flask.app.routes.main_routes import main_bp
    app.register_blueprint(main_bp, url_prefix="/api")

    from abundance_flask.app.routes.proxy_route import proxy_bp
    app.register_blueprint(proxy_bp, url_prefix="/api")

    from abundance_flask.app.routes.web_route import web_bp
    app.register_blueprint(web_bp)

    from abundance_flask.app.routes.entry_route import entry_bp
    app.register_blueprint(entry_bp, url_prefix="/api")

    # 创建表
    with app.app_context():
        from abundance_flask.app.models import entry_model
        print(db.metadata.tables.keys())
        db.create_all()

    return app