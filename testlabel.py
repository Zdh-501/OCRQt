import os
import sys
import subprocess
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtCore import QThread

class WorkerThread(QThread):
    def __init__(self, command, working_dir):
        super().__init__()
        self.command = command
        self.working_dir = working_dir

    def run(self):
        subprocess.run(self.command, cwd=self.working_dir)

class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('PPOCRLabel Integration')
        self.setGeometry(100, 100, 800, 600)

        self.startButton = QPushButton('Start PPOCRLabel', self)
        self.startButton.clicked.connect(self.startPPOCRLabel)

        layout = QVBoxLayout()
        layout.addWidget(self.startButton)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

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
    ex = MainApp()
    ex.show()
    sys.exit(app.exec_())
