from PyQt5.QtWidgets import (QApplication, QWidget, QLineEdit, QComboBox,
                             QCheckBox, QSpinBox, QTextEdit, QPushButton,
                             QLabel, QGridLayout, QVBoxLayout, QHBoxLayout, QGroupBox, QFileDialog)

class ModelTrainingInterface(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        # 创建控件
        self.datasetEdit = QLineEdit()
        self.valsetEdit = QLineEdit()
        self.modelCombo = QComboBox()
        self.optimizerCombo = QComboBox()
        self.epochSpin = QSpinBox()
        self.gpuCheck = QCheckBox("启用GPU训练")
        self.logText = QTextEdit()
        self.trainButton = QPushButton("训练")
        self.testButton = QPushButton("测试")

        # 设置布局
        grid = QGridLayout()
        grid.addWidget(QLabel('训练集'), 0, 0)
        grid.addWidget(self.datasetEdit, 0, 1)
        grid.addWidget(QLabel('验证集'), 1, 0)
        grid.addWidget(self.valsetEdit, 1, 1)
        grid.addWidget(QLabel('模型结构'), 2, 0)
        grid.addWidget(self.modelCombo, 2, 1)
        grid.addWidget(QLabel('优化器'), 3, 0)
        grid.addWidget(self.optimizerCombo, 3, 1)
        grid.addWidget(QLabel('迭代次数'), 4, 0)
        grid.addWidget(self.epochSpin, 4, 1)
        grid.addWidget(self.gpuCheck, 5, 1)

        # 按钮布局
        hbox = QHBoxLayout()
        hbox.addWidget(self.trainButton)
        hbox.addWidget(self.testButton)

        # 日志布局
        vbox = QVBoxLayout()
        vbox.addWidget(QLabel('训练日志'))
        vbox.addWidget(self.logText)

        # 主布局
        mainLayout = QVBoxLayout()
        mainLayout.addLayout(grid)
        mainLayout.addLayout(hbox)
        mainLayout.addLayout(vbox)

        self.setLayout(mainLayout)

        # 设置窗口
        self.setWindowTitle('模型训练界面')
        self.show()

# 创建应用实例和窗口
app = QApplication([])
window = ModelTrainingInterface()
app.exec_()
