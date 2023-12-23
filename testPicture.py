import sys
import requests
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QPushButton, QListView, QVBoxLayout, QWidget, QMessageBox
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import QTimer

class YourMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.setupPolling()

    def initUI(self):
        self.setWindowTitle('Task Fetcher')
        self.setGeometry(100, 100, 600, 400)

        # 中央部件和布局
        centralWidget = QWidget(self)
        self.setCentralWidget(centralWidget)
        layout = QVBoxLayout(centralWidget)

        # API 地址输入框
        self.apiInput = QLineEdit(self)
        self.apiInput.setPlaceholderText("Enter API URL")
        layout.addWidget(self.apiInput)

        # 获取数据按钮
        self.fetchButton = QPushButton('Fetch Tasks', self)
        self.fetchButton.clicked.connect(self.fetchData)
        layout.addWidget(self.fetchButton)

        # 任务列表视图
        self.taskListView = QListView(self)
        self.taskModel = QStandardItemModel(self.taskListView)
        self.taskListView.setModel(self.taskModel)
        layout.addWidget(self.taskListView)

    def setupPolling(self):
        self.pollingTimer = QTimer(self)
        self.pollingTimer.timeout.connect(self.fetchData)
        self.pollingTimer.start(5000)  # 每 5 秒执行一次 fetchData

    def fetchData(self):
        api_url = self.apiInput.text().strip()
        if api_url:
            tasks = self.fetch_task_data(api_url)
            if tasks:
                self.processTaskData(tasks)

    def fetch_task_data(self, api_url):
        try:
            response = requests.get(api_url)
            response.raise_for_status()
            return response.json()  # 假设 API 返回 JSON 数据
        except requests.RequestException as e:
            QMessageBox.critical(self, 'Error', f'Error fetching tasks: {e}')
            return None

    def processTaskData(self, tasks):
        self.taskModel.clear()  # 清除旧数据
        for task in tasks:
            # 假设 task 包含多个属性，可根据需要调整
            task_info = "批号：{}\n物料类型：{}\n产品物料名称：{}\n生产日期：{}\n有效期至：{}\n产线：{}\n任务序号：{}\n检测数量：{}".format(
                task["批号"], task["物料类型"], task["产品物料名称"], task["生产日期"],
                task["有效期至"], task["产线"], task["任务序号"], task["检测数量"]
            )
            item = QStandardItem(task_info)
            self.taskModel.appendRow(item)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = YourMainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
