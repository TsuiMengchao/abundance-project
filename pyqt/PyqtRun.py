import os
import sys

from PyQt5 import QtWidgets

from pyqt.src.PyqtController import PyqtController


class PyQtRun:
    def __init__(self):
        app = QtWidgets.QApplication(sys.argv)

        PyqtController()

        os._exit(app.exec_())