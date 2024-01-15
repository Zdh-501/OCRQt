import sys

from PyQt5.QtWidgets import QApplication
from pyqt5_plugins.examplebutton import QtWidgets

from ui.layout.UI_LogPage import Ui_LogPage

class LogPage(QtWidgets.QWidget,Ui_LogPage):
    def __init__(self):
        super(LogPage, self).__init__()
        self.setupUi(self)  # 从UI_DataCollectPage.py中加载UI定义

    #todo 添加错误信息

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = LogPage()
    mainWindow.show()
    app.exec_()