import sys
from PyQt5.QtWidgets import QApplication
from pyqt5_plugins.examplebutton import QtWidgets

from ui.layout.UI_DataCollectPage import Ui_DataCollectPage

class DataCollectPage(QtWidgets.QWidget,Ui_DataCollectPage):
    def __init__(self):
        super(DataCollectPage, self).__init__()
        self.setupUi(self)  # 从UI_DataCollectPage.py中加载UI定义


# if __name__ == '__main__':
# app = QApplication(sys.argv)
# mainWindow = DataCollectPage()
# mainWindow.show()
# app.exec_()