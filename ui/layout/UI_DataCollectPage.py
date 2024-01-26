# -*- coding: utf-8 -*-

# DataCollectPage implementation generated from reading ui file 'UI_DataCollectPage.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QSlider, QStyle, QStyleOptionSlider
from PyQt5.QtCore import QRect, QPoint, Qt
class CustomSlider(QSlider):
    def __init__(self, orientation, parent=None):
        super(CustomSlider, self).__init__(orientation, parent)

    def mousePressEvent(self, event):
        # 获取滑块的位置
        handle_pos = self.handlePosition()

        # 获取鼠标点击的位置
        click_pos = event.pos().x() if self.orientation() == Qt.Horizontal else event.pos().y()

        # 计算滑块宽度（或高度）
        handle_width = self.style().pixelMetric(QStyle.PM_SliderThickness, None, self)

        # 检查鼠标点击是否在滑块上
        if abs(handle_pos - click_pos) <= handle_width / 2:
            # 如果在滑块上，则调用父类方法处理点击事件
            super(CustomSlider, self).mousePressEvent(event)
        else:
            # 如果不在滑块上，忽略点击事件
            event.ignore()

    def handlePosition(self):
        opt = QStyleOptionSlider()
        self.initStyleOption(opt)
        rect = self.style().subControlRect(QStyle.CC_Slider, opt, QStyle.SC_SliderHandle, self)
        return rect.center().x() if self.orientation() == Qt.Horizontal else rect.center().y()

class Ui_DataCollectPage(object):
    def setupUi(self, DataCollectPage):
        DataCollectPage.setObjectName("DataCollectPage")
        DataCollectPage.resize(977, 466)
        self.horizontalLayout = QtWidgets.QHBoxLayout(DataCollectPage)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.widget_1 = QtWidgets.QWidget(DataCollectPage)
        self.widget_1.setObjectName("widget_1")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.widget_1)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_5 = QtWidgets.QLabel(self.widget_1)
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_2.addWidget(self.label_5)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        self.horizontalLayout.addWidget(self.widget_1)
        self.widget_2 = QtWidgets.QWidget(DataCollectPage)
        self.widget_2.setObjectName("widget_2")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget_2)
        self.verticalLayout.setObjectName("verticalLayout")
        self.widget_3 = QtWidgets.QWidget(self.widget_2)
        self.widget_3.setObjectName("widget_3")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.widget_3)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_1 = QtWidgets.QLabel(self.widget_3)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_1.setFont(font)
        self.label_1.setObjectName("label_1")
        self.horizontalLayout_4.addWidget(self.label_1)
        self.countLabel = QtWidgets.QLabel(self.widget_3)
        self.countLabel.setObjectName("countLabel")
        self.horizontalLayout_4.addWidget(self.countLabel)
        self.zeroButton = QtWidgets.QPushButton(self.widget_3)
        self.zeroButton.setObjectName("zeroButton")
        self.horizontalLayout_4.addWidget(self.zeroButton)
        self.horizontalLayout_4.setStretch(0, 1)
        self.horizontalLayout_4.setStretch(1, 1)
        self.verticalLayout_2.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_4 = QtWidgets.QLabel(self.widget_3)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_5.addWidget(self.label_4)
        self.formatBox = QtWidgets.QComboBox(self.widget_3)
        self.formatBox.setObjectName("formatBox")
        self.formatBox.addItem("")
        self.formatBox.addItem("")
        self.horizontalLayout_5.addWidget(self.formatBox)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem)
        self.horizontalLayout_5.setStretch(0, 2)
        self.horizontalLayout_5.setStretch(1, 3)
        self.horizontalLayout_5.setStretch(2, 1)
        self.verticalLayout_2.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_3 = QtWidgets.QLabel(self.widget_3)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_3.addWidget(self.label_3)
        self.saveEdit = QtWidgets.QLineEdit(self.widget_3)
        self.saveEdit.setObjectName("saveEdit")
        self.horizontalLayout_3.addWidget(self.saveEdit)
        self.saveButton = QtWidgets.QPushButton(self.widget_3)
        self.saveButton.setObjectName("saveButton")
        self.horizontalLayout_3.addWidget(self.saveButton)
        self.horizontalLayout_3.setStretch(0, 2)
        self.horizontalLayout_3.setStretch(1, 3)
        self.horizontalLayout_3.setStretch(2, 1)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.label_8 = QtWidgets.QLabel(self.widget_3)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")
        self.verticalLayout_2.addWidget(self.label_8)
        self.nameEdit = QtWidgets.QLineEdit(self.widget_3)
        self.nameEdit.setObjectName("nameEdit")
        self.verticalLayout_2.addWidget(self.nameEdit)
        self.verticalLayout.addWidget(self.widget_3)
        self.widget_4 = QtWidgets.QWidget(self.widget_2)
        self.widget_4.setObjectName("widget_4")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.widget_4)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.label_6 = QtWidgets.QLabel(self.widget_4)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.verticalLayout_4.addWidget(self.label_6)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.normMixBox = QtWidgets.QCheckBox(self.widget_4)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.normMixBox.setFont(font)
        self.normMixBox.setTristate(False)
        self.normMixBox.setObjectName("normMixBox")
        self.horizontalLayout_6.addWidget(self.normMixBox)
        self.kdBox = QtWidgets.QCheckBox(self.widget_4)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.kdBox.setFont(font)
        self.kdBox.setObjectName("kdBox")
        self.horizontalLayout_6.addWidget(self.kdBox)
        self.verticalLayout_4.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.label_7 = QtWidgets.QLabel(self.widget_4)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.horizontalLayout_7.addWidget(self.label_7)
        self.exposureValueLabel = QtWidgets.QLabel(self.widget_4)
        self.exposureValueLabel.setText("")
        self.exposureValueLabel.setObjectName("exposureValueLabel")
        self.horizontalLayout_7.addWidget(self.exposureValueLabel)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem1)
        self.verticalLayout_4.addLayout(self.horizontalLayout_7)
        self.exposureSlider = CustomSlider(Qt.Horizontal,self.widget_4)
        self.exposureSlider.setOrientation(QtCore.Qt.Horizontal)
        self.exposureSlider.setObjectName("exposureSlider")
        self.verticalLayout_4.addWidget(self.exposureSlider)
        self.verticalLayout.addWidget(self.widget_4)
        self.widget_5 = QtWidgets.QWidget(self.widget_2)
        self.widget_5.setObjectName("widget_5")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.widget_5)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.startButton = QtWidgets.QToolButton(self.widget_5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.startButton.sizePolicy().hasHeightForWidth())
        self.startButton.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Adobe 黑体 Std R")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.startButton.setFont(font)
        self.startButton.setObjectName("startButton")
        self.verticalLayout_6.addWidget(self.startButton)
        spacerItem2 = QtWidgets.QSpacerItem(20, 41, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_6.addItem(spacerItem2)
        self.takepictureButton = QtWidgets.QToolButton(self.widget_5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.takepictureButton.sizePolicy().hasHeightForWidth())
        self.takepictureButton.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Adobe 黑体 Std R")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.takepictureButton.setFont(font)
        self.takepictureButton.setObjectName("takepictureButton")
        self.verticalLayout_6.addWidget(self.takepictureButton)
        spacerItem3 = QtWidgets.QSpacerItem(20, 41, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_6.addItem(spacerItem3)
        self.labelButton = QtWidgets.QToolButton(self.widget_5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelButton.sizePolicy().hasHeightForWidth())
        self.labelButton.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Adobe 黑体 Std R")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.labelButton.setFont(font)
        self.labelButton.setObjectName("labelButton")
        self.verticalLayout_6.addWidget(self.labelButton)
        self.verticalLayout_6.setStretch(0, 2)
        self.verticalLayout_6.setStretch(1, 1)
        self.verticalLayout_6.setStretch(2, 4)
        self.verticalLayout_6.setStretch(3, 1)
        self.verticalLayout_6.setStretch(4, 2)
        self.verticalLayout.addWidget(self.widget_5)
        self.verticalLayout.setStretch(0, 1)
        self.verticalLayout.setStretch(1, 1)
        self.verticalLayout.setStretch(2, 4)
        self.horizontalLayout.addWidget(self.widget_2)
        self.horizontalLayout.setStretch(0, 5)
        self.horizontalLayout.setStretch(1, 2)

        self.retranslateUi(DataCollectPage)
        QtCore.QMetaObject.connectSlotsByName(DataCollectPage)

    def retranslateUi(self, DataCollectPage):
        _translate = QtCore.QCoreApplication.translate
        DataCollectPage.setWindowTitle(_translate("DataCollectPage", "DataCollectPage"))
        self.label_5.setText(_translate("DataCollectPage", "相机画面"))
        self.label_1.setText(_translate("DataCollectPage", "已拍张数："))
        self.countLabel.setText(_translate("DataCollectPage", "0"))
        self.zeroButton.setText(_translate("DataCollectPage", "清零"))
        self.label_4.setText(_translate("DataCollectPage", "导出格式："))
        self.formatBox.setItemText(0, _translate("DataCollectPage", "png"))
        self.formatBox.setItemText(1, _translate("DataCollectPage", "jpg"))
        self.label_3.setText(_translate("DataCollectPage", "保存路径："))
        self.saveButton.setText(_translate("DataCollectPage", "选择"))
        self.label_8.setText(_translate("DataCollectPage", "图片命名："))
        self.label_6.setText(_translate("DataCollectPage", "采集通道："))
        self.normMixBox.setText(_translate("DataCollectPage", "normMix通道"))
        self.kdBox.setText(_translate("DataCollectPage", "kd通道"))
        self.label_7.setText(_translate("DataCollectPage", "曝光值："))
        self.startButton.setText(_translate("DataCollectPage", "启动相机"))
        self.takepictureButton.setText(_translate("DataCollectPage", "拍照"))
        self.labelButton.setText(_translate("DataCollectPage", "标注数据"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    DataCollectPage = QtWidgets.QWidget()
    ui = Ui_DataCollectPage()
    ui.setupUi(DataCollectPage)
    DataCollectPage.show()
    sys.exit(app.exec_())
