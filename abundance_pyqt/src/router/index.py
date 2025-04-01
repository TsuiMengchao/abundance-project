from abundance.pyqt.router import Router
from abundance_pyqt.src.router.modules.page import page_routes


class RouterIndex:
    # 类属性，用于保存单例实例
    _instance = None

    def __new__(cls, app):
        # 如果实例还未创建，则创建一个新实例
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls.router = Router(app, page_routes)
        return cls._instance.router