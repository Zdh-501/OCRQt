import os
import subprocess
import sys

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

        self.labelButton.clicked.connect(self.startPPOCRLabel)

    def startPPOCRLabel(self):
        # 获取当前文件所在的目录
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # 设置 PPOCRLabel 的工作目录为 PaddleOCR 文件夹
        working_dir = os.path.join(current_dir, 'PaddleOCR')
        # PPOCRLabel 的命令，假设 PPOCRLabel 是一个可执行的文件或者正确配置了环境变量
        command = ['PPOCRLabel', '--lang', 'ch']

        self.workerThread = WorkerThread(command, working_dir)
        self.workerThread.start()
if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = DataCollectPage()
    mainWindow.show()
    app.exec_()