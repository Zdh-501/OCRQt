import os
import subprocess
import sys
import json  # 导入json模块

from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import QApplication
from pyqt5_plugins.examplebutton import QtWidgets

from ui.layout.UI_DataCollectPage import Ui_DataCollectPage
class WorkerThread(QThread):
    def __init__(self, command, working_dir):
        super().__init__()
        self.command = command
        self.working_dir = working_dir

    def run(self):
        subprocess.run(self.command, cwd=self.working_dir)
class DataCollectPage(QtWidgets.QWidget,Ui_DataCollectPage):
    def __init__(self):
        super(DataCollectPage, self).__init__()
        self.setupUi(self)  # 从UI_DataCollectPage.py中加载UI定义
        #todo 读取配置文件 此处要改成绝对路径
        with open('E:\\Desktop\\OCRQT\\config.json', 'r') as config_file:
            self.config = json.load(config_file)
        self.labelButton.clicked.connect(self.startPPOCRLabel)

    def startPPOCRLabel(self):
        # 直接使用配置文件中的绝对路径
        working_dir = self.config["PPOCRLabel_working_dir"]
        command = ['PPOCRLabel', '--lang', 'ch']

        self.workerThread = WorkerThread(command, working_dir)
        self.workerThread.start()
if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = DataCollectPage()
    mainWindow.show()
    app.exec_()