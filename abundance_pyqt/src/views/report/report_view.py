import logging

from PyQt6.QtWidgets import QWidget, QPushButton

from autotest_common.config.report_config import ReportConfig
from abundance_pyqt.src.api.report import get_list
from abundance_pyqt.src.utils.ui_assets_loader import UiAssetsLoader
from abundance_pyqt.src.views.report.report import Ui_Form

logger = logging.getLogger(__name__)

class ReportView(QWidget, Ui_Form):
    """
    主窗口视图类，继承自 QMainWindow 和 Ui_MainWindow
    """
    def __init__(self):
        super(ReportView, self).__init__()
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
        report_list, error = get_list()
        self.initReportList(report_list)
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
    def initReportList(self, report_list):
        index = 0
        report_list_button = []
        for report in report_list:
            report_list_button.append(QPushButton(report))
            report_config = ReportConfig()
            report_list_button[index].clicked.connect(lambda: UiAssetsLoader.load_html(self.webEngineView, f"http://{report_config.host}:{report_config.port}/{report}/html"))
            self.verticalLayout_3.addWidget(report_list_button[index])
            index+=1
        if report_list_button:
            report_list_button[0].click()

    # endregion

    # region Common

    # endregion


if __name__ == '__main__':
    import sys
    import os
    from PyQt6 import QtWidgets
    app = QtWidgets.QApplication(sys.argv)
    ui = ReportView()
    ui.show()
    os._exit(app.exec())
