import os
from dotenv import load_dotenv

# 加载.env文件中的环境变量
load_dotenv()

class BaseConfig:
    """基础配置（所有环境共享）"""
    SECRET_KEY = os.getenv("SECRET_KEY", "your-default-secret-key")
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # 关闭不必要的警告