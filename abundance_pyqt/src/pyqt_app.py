import logging

from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QMainWindow
logger = logging.getLogger(__name__)

class PyQtApp:
    # 类属性，用于保存单例实例
    _instance = None

    def __new__(cls):
        # 如果实例还未创建，则创建一个新实例
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.get_window()
        return cls._instance

    def use(self, obj):
        setattr(self._instance, obj.__name__, obj)

    def get_window(self):
        self.page = QMainWindow()
        self.page.setObjectName("page")
        self.page.resize(900, 650)
        centralwidget = QtWidgets.QWidget(parent=self.page)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred,
                                           QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(centralwidget.sizePolicy().hasHeightForWidth())
        centralwidget.setSizePolicy(sizePolicy)
        centralwidget.setObjectName("centralwidget")
        self.router_layout = QtWidgets.QGridLayout(centralwidget)
        self.router_layout.setContentsMargins(0, 0, 0, 0)
        self.router_layout.setSpacing(0)
        self.router_layout.setObjectName("layout")
        self.page.setCentralWidget(centralwidget)