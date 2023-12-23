from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QHBoxLayout


class TaskDialogUI(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 设置窗口标志以去除问号
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)

        self.setWindowTitle("开始检测")  # 设置窗口标题
        layout = QVBoxLayout()

        # 设置对话框大小
        self.resize(300, 150)  # 可以根据需要调整这些值

        # 添加用于显示任务信息的标签
        self.taskLabel = QLabel("检测任务：", self)
        layout.addWidget(self.taskLabel)

        # 创建水平布局用于放置按钮
        buttonLayout = QHBoxLayout()

        # 添加确认和取消按钮
        self.okButton = QPushButton("确认", self)
        buttonLayout.addWidget(self.okButton)
        self.cancelButton = QPushButton("取消", self)
        buttonLayout.addWidget(self.cancelButton)

        # 将按钮布局添加到主布局
        layout.addLayout(buttonLayout)

        self.setLayout(layout)
