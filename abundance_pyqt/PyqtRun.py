import os
import sys

from PyQt5 import QtWidgets

from abundance_pyqt.src.pyqt_app import PyQtApp
from abundance_pyqt.src.router.index import RouterIndex


class PyQtRun:
    def __init__(self):
        app = QtWidgets.QApplication(sys.argv)

        pyqt_app = PyQtApp()
        router = RouterIndex(pyqt_app)

        pyqt_app.use(router)

        sys.exit(app.exec())