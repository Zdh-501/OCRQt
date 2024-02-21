import sys

from PyQt5 import QtWidgets, QtGui


from SQL.dbFunction import *
from ui.impl.LoginDialog import *

from SQL.dbFunction import *
from ui.layout.UI_LogPage import Ui_LogPage

class LogPage(QtWidgets.QWidget,Ui_LogPage):
    def __init__(self):
        super(LogPage, self).__init__()
        self.setupUi(self)  # 从UI_DataCollectPage.py中加载UI定义
        # 启用表格排序功能
        self.tableWidget.setSortingEnabled(True)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = LogPage()
    mainWindow.show()
    app.exec_()