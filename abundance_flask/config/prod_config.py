from abundance_flask.config.base_config import BaseConfig

class ProductionConfig(BaseConfig):
    """开发环境配置"""
    DEBUG = True
    # 开发环境数据库（示例：SQLite，也可换MySQL/PostgreSQL）
    SQLALCHEMY_DATABASE_URI = "sqlite:///dev.db"