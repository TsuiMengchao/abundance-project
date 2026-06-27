import os

from abundance_flask.config.base_config import BaseConfig

class DevelopmentConfig(BaseConfig):
    """开发环境配置"""
    DEBUG = True
    # 开发环境数据库（示例：SQLite）
    # 固定数据库绝对路径
    base_dir = os.path.abspath(os.path.dirname(__file__))
    db_file = os.path.join(base_dir, "entry.db")
    # db文件夹不存在，直接创建失败
    os.makedirs(os.path.dirname(db_file), exist_ok=True)
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{db_file}"