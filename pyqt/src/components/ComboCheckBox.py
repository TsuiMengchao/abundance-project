from PyQt5 import QtCore
from PyQt5.QtWidgets import QComboBox, QLineEdit, QListWidget, QCheckBox, QListWidgetItem, QApplication
from PyQt5.QtCore import pyqtSignal
import sys

"""
1.将show函数改成show0
2.增加changeitemlist函数
3.增加信号signa
"""


class ComboCheckBox(QComboBox):
    signa = pyqtSignal(list)

    def __init__(self):  # items==[str,str...]
        super(ComboCheckBox, self).__init__()
        self.items = None

        self.Selectedrow_num = 0
        self.qCheckBox = []
        self.qLineEdit = QLineEdit()
        self.qLineEdit.setReadOnly(True)
        self.qListWidget = QListWidget()


        self.setModel(self.qListWidget.model())
        self.setView(self.qListWidget)
        self.setLineEdit(self.qLineEdit)
        self.setMaxVisibleItems(100)  # 避免滑条的出现引起滑条偷吃标签的问题

        self.Outputlist = []

    def setupUi(self, items):
        self.items = list(items)
        self.items.insert(0, '全部')

        self.row_num = len(self.items)

        self.qCheckBox = []
        self.qListWidget.clear()
        self.addQCheckBox(0)
        self.qCheckBox[0].stateChanged.connect(self.All)

        for i in range(1, self.row_num):
            self.addQCheckBox(i)
            self.qCheckBox[i].stateChanged.connect(self.show0)

    def addQCheckBox(self, i):
        self.qCheckBox.append(QCheckBox())
        qItem = QListWidgetItem(self.qListWidget)
        self.qCheckBox[i].setText(self.items[i])
        self.qListWidget.setItemWidget(qItem, self.qCheckBox[i])

        # 设置尺寸策略，让项的高度自适应内容（可根据实际情况调整合适的高度值）
        qItem.setSizeHint(QtCore.QSize(0, 50))  # 这里将高度设置为30像素，你可以修改这个值

        font = self.qCheckBox[i].font()
        font.setPointSize(10)  # 设置合适的字体大小，可根据实际情况调整
        self.qCheckBox[i].setFont(font)

    def Selectlist(self):
        for i in range(1, self.row_num):
            item = self.qCheckBox[i].text()
            if self.qCheckBox[i].isChecked() == True:
                if item not in self.Outputlist:
                    self.Outputlist.append(item)
            else:
                if item in self.Outputlist:
                    self.Outputlist.remove(item)
        self.Selectedrow_num = len(self.Outputlist)

        return self.Outputlist

    def text(self):
        return self.qLineEdit.text()

    def show0(self):
        show0 = ''
        Outputlist = self.Selectlist()
        self.signa.emit(Outputlist)
        self.qLineEdit.setReadOnly(False)
        self.qLineEdit.clear()

        if len(Outputlist) == 1:
            show0 = Outputlist[0]
        elif len(Outputlist) > 1:
            for i, item in enumerate(Outputlist):
                if i < len(Outputlist) - 1:
                    show0 += item + ' '
                else:
                    show0 += item
        else:
            self.qCheckBox[0].setCheckState(0)

        if len(Outputlist) == self.row_num - 1:
            self.qCheckBox[0].setCheckState(2)
        elif len(Outputlist) > 0 and len(Outputlist) < self.row_num - 1:
            self.qCheckBox[0].setCheckState(1)

        self.qLineEdit.setText(show0)
        self.qLineEdit.setReadOnly(True)

    def All(self, zhuangtai):
        if zhuangtai == 2:
            for i in range(1, self.row_num):
                self.qCheckBox[i].setChecked(True)
        elif zhuangtai == 1:
            if self.Selectedrow_num == 0:
                self.qCheckBox[0].setCheckState(2)
        elif zhuangtai == 0:
            self.clear()

    def clear(self):
        for i in range(self.row_num):
            self.qCheckBox[i].setChecked(False)

    def changeitemlist(self, itemlist):

        self.items = itemlist
        self.items.insert(0, '全部')
        self.row_num = len(self.items)

        self.Selectedrow_num = 0
        self.qCheckBox = []
        self.qLineEdit = QLineEdit()
        self.qLineEdit.setReadOnly(True)
        self.qListWidget = QListWidget()
        self.addQCheckBox(0)
        self.qCheckBox[0].stateChanged.connect(self.All)
        for i in range(1, self.row_num):
            self.addQCheckBox(i)
            self.qCheckBox[i].stateChanged.connect(self.show0)
        self.setModel(self.qListWidget.model())
        self.setView(self.qListWidget)
        self.setLineEdit(self.qLineEdit)