import logging

from PyQt6.QtWidgets import QWidget

from abundance_pyqt.src.views.setting.setting import Ui_Form

logger = logging.getLogger(__name__)

class SettingView(QWidget, Ui_Form):
    """
    主窗口视图类，继承自 QMainWindow 和 Ui_MainWindow
    """
    def __init__(self):
        super(SettingView, self).__init__()
        # 加载页面
        self.setupUi(self)
        # 初始化UI
        self.initUi()
        # 初始化全局参数
        self.initParams()
        # 初始化全局槽连接
        self.initSlot()
        # 初始化外部回调动作
        self.initAction()
    def initUi(self):
        """
        初始化UI界面的方法
        """
        pass

    def initParams(self):
        """
        初始化全局参数的方法
        """
        pass

    def initSlot(self):
        """
        初始化信号与槽连接的方法
        """
        pass

    def initAction(self):
        """
        初始化外部回调动作的方法
        """
        pass

    # region Slot

    # endregion

    # region Def

    # endregion

    # region Common

    # endregion


if __name__ == '__main__':
    import sys
    import os
    from PyQt6 import QtWidgets
    app = QtWidgets.QApplication(sys.argv)
    ui = SettingView()
    ui.show()
    os._exit(app.exec())
