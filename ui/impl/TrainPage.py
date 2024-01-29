import sys

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QTableWidgetItem, QApplication

from ui.layout.UI_TrainPage import Ui_TrainPage
from PyQt5 import QtCore, QtWidgets

class TrainPage(QtWidgets.QWidget,Ui_TrainPage):

    def __init__(self):
        super(TrainPage, self).__init__()
        self.setupUi(self)  # 从UI_TaskPage.py中加载UI定义

# if __name__ == '__main__':
# app = QApplication(sys.argv)
# mainWindow = TrainPage()
# mainWindow.show()
# app.exec_()