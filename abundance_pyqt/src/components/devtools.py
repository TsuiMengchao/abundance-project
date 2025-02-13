from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton, QHBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage, QWebEngineSettings


class DevTools(QMainWindow):
    def __init__(self, web_view, enable=True):
        super().__init__()
        self.web_view = web_view
        self.enable = enable
        self.setup_devtools()

    def setup_devtools(self):
        # 启用开发者工具
        settings = self.web_view.settings()
        try:
            # 尝试新版设置方式
            settings.setAttribute(QWebEngineSettings.DeveloperExtrasEnabled, True)
        except AttributeError:
            try:
                # 尝试旧版枚举值方式
                settings.setAttribute(QWebEngineSettings.WebAttribute(12), True)
            except AttributeError:
                print("无法启用开发者工具，请检查 PyQt 版本。")

        # 创建开发者工具窗口部件
        self.devtools_widget = QWidget()
        self.devtools_layout = QVBoxLayout()
        self.devtools_web_view = QWebEngineView()
        self.devtools_page = QWebEnginePage()
        self.devtools_web_view.setPage(self.devtools_page)

        # 关联主页面和开发者工具页面
        self.web_view.page().setDevToolsPage(self.devtools_page)

        # 点击按钮触发检查元素动作
        self.web_view.page().triggerAction(QWebEnginePage.InspectElement)

        # 设置开发者工具窗口布局
        self.devtools_layout.addWidget(self.devtools_web_view)

        # 创建主窗口的布局
        central_widget = QWidget()
        main_layout = QVBoxLayout()
        main_layout.addLayout(self.devtools_layout)
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def keyPressEvent(self, event):
        if self.enable:
            if event.key() == Qt.Key_F12:
                if self.isHidden():
                    self.show()
                else:
                    self.hide()
        super().keyPressEvent(event)