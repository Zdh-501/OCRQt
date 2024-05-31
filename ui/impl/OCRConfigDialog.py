from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QLineEdit, QCheckBox, QComboBox,
    QDialogButtonBox, QPushButton, QFileDialog, QHBoxLayout
)

class OCRConfigDialog(QDialog):
    def __init__(self, parent=None):
        super(OCRConfigDialog, self).__init__(parent)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.layout = QVBoxLayout(self)

        self.setWindowTitle("配置 OCR 参数")

        # 默认路径
        self.default_det_path = "D:/Paddle/inference_model/det/ResNet50_1220"
        self.default_rec_path = "D:/Paddle/inference_model/rec/rec240108"

        # 创建检测模型路径的水平布局
        self.detModelPathLayout = QHBoxLayout()
        self.detModelPathEdit = QLineEdit(self.default_det_path, self)
        self.detPathButton = QPushButton("选择", self)
        self.detPathButton.clicked.connect(self.selectDetModelPath)
        self.detModelPathLayout.addWidget(self.detModelPathEdit)
        self.detModelPathLayout.addWidget(self.detPathButton)

        # 创建识别模型路径的水平布局
        self.recModelPathLayout = QHBoxLayout()
        self.recModelPathEdit = QLineEdit(self.default_rec_path, self)
        self.recPathButton = QPushButton("选择", self)
        self.recPathButton.clicked.connect(self.selectRecModelPath)
        self.recModelPathLayout.addWidget(self.recModelPathEdit)
        self.recModelPathLayout.addWidget(self.recPathButton)

        # 将布局添加到对话框的垂直布局中
        self.layout.addWidget(QLabel("检测模型路径:"))
        self.layout.addLayout(self.detModelPathLayout)
        self.layout.addWidget(QLabel("识别模型路径:"))
        self.layout.addLayout(self.recModelPathLayout)

        # 创建用于 "使用角度分类" 的复选框
        self.useAngleClsCheckbox = QCheckBox("使用角度分类", self)
        self.useAngleClsCheckbox.setChecked(False)
        self.layout.addWidget(self.useAngleClsCheckbox)

        # 创建解剪比率的输入框
        self.unclipRatioEdit = QLineEdit("2.8", self)
        self.layout.addWidget(QLabel("解剪比率:"))
        self.layout.addWidget(self.unclipRatioEdit)

        # 创建语言选择的下拉菜单
        self.langComboBox = QComboBox(self)
        self.langComboBox.addItems(["ch", "en"])  # 添加支持的语言选项
        self.layout.addWidget(QLabel("语言:"))
        self.layout.addWidget(self.langComboBox)

        # 创建对话框的按钮
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        self.buttonBox.button(QDialogButtonBox.Ok).setText("确认")
        self.buttonBox.button(QDialogButtonBox.Cancel).setText("取消")
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        self.layout.addWidget(self.buttonBox)

        # 调整布局和控件后，设置固定大小
        #self.layout.setSizeConstraint(QVBoxLayout.SetFixedSize)

        # 设置对话框的尺寸，拉长窗口的长度
        self.resize(600, self.height())  # 宽度设置为600，高度保持不变

    # 槽函数用于选择检测模型路径
    def selectDetModelPath(self):
        folder_path = QFileDialog.getExistingDirectory(self, "选择检测模型文件夹", self.default_det_path)
        if folder_path:
            self.detModelPathEdit.setText(folder_path)

    # 槽函数用于选择识别模型路径
    def selectRecModelPath(self):
        folder_path = QFileDialog.getExistingDirectory(self, "选择识别模型文件夹", self.default_rec_path)
        if folder_path:
            self.recModelPathEdit.setText(folder_path)

    def getConfig(self):
        # 获取用户输入并返回配置字典
        return {
            'det_model_dir': self.detModelPathEdit.text(),
            'rec_model_dir': self.recModelPathEdit.text(),
            'use_angle_cls': self.useAngleClsCheckbox.isChecked(),
            'det_db_unclip_ratio': float(self.unclipRatioEdit.text()),
            'lang': self.langComboBox.currentText()
        }
