from abundance_flask.config.base_config import BaseConfig
from abundance_flask.config.dev_config import DevelopmentConfig
from abundance_flask.config.prod_config import ProductionConfig

# 配置映射（环境名 -> 配置类）
config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig
}