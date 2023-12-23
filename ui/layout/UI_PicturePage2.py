# -*- coding: utf-8 -*-

# PicturePage implementation generated from reading ui file 'UI_PicturePage2.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal


class ClickableProgressBar(QtWidgets.QProgressBar):
    clickedValue = pyqtSignal(int)

    def __init__(self, parent=None):
        super(ClickableProgressBar, self).__init__(parent)
        self.segmentCount = 0  # 初始段数

    def setSegmentCount(self, count):
        self.segmentCount = count
        self.update()  # 强制更新控件，这将调用 paintEvent 方法
    def mousePressEvent(self, event):
        super(ClickableProgressBar, self).mousePressEvent(event)
        if event.button() == QtCore.Qt.LeftButton:
            # 计算点击位置对应的进度值
            clickValue = int((event.x() / self.width()) * self.maximum())
            self.clickedValue.emit(clickValue)

    def paintEvent(self, event):
        super(ClickableProgressBar, self).paintEvent(event)
        painter = QtGui.QPainter(self)
        pen = QtGui.QPen(QtGui.QColor(0, 0, 0))  # 黑色笔刷
        painter.setPen(pen)

        # 绘制分段标记
        if self.segmentCount > 0:
            segment_width = self.width() / self.segmentCount
            for i in range(1, self.segmentCount):
                x = segment_width * i
                # 绘制分段线
                painter.drawLine(x, 0, x, self.height())
                # 如果需要，在每个分段处添加文本标签
                # painter.drawText(x - 10, self.height() / 2, str(i))

        painter.end()
class Ui_PicturePage2(object):
    def setupUi(self, PicturePage):
        PicturePage.setObjectName("PicturePage")
        PicturePage.resize(989, 641)
        self.horizontalLayout = QtWidgets.QHBoxLayout(PicturePage)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.widget_1 = QtWidgets.QWidget(PicturePage)
        self.widget_1.setObjectName("widget_1")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.widget_1)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.stackedWidget = QtWidgets.QStackedWidget(self.widget_1)
        self.stackedWidget.setObjectName("stackedWidget")
        self.verticalLayout_3.addWidget(self.stackedWidget)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.progressBar = ClickableProgressBar(self.widget_1)
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        self.horizontalLayout_2.addWidget(self.progressBar)
        self.pushButton = QtWidgets.QPushButton(self.widget_1)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout_2.addWidget(self.pushButton)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        self.horizontalLayout.addWidget(self.widget_1)
        self.widget_2 = QtWidgets.QWidget(PicturePage)
        self.widget_2.setObjectName("widget_2")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget_2)
        self.verticalLayout.setObjectName("verticalLayout")
        self.widget_3 = QtWidgets.QWidget(self.widget_2)
        self.widget_3.setObjectName("widget_3")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.widget_3)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.widget_7 = QtWidgets.QWidget(self.widget_3)
        self.widget_7.setObjectName("widget_7")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.widget_7)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.textBrowser_2 = QtWidgets.QTextBrowser(self.widget_7)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textBrowser_2.sizePolicy().hasHeightForWidth())
        self.textBrowser_2.setSizePolicy(sizePolicy)
        self.textBrowser_2.setMinimumSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.textBrowser_2.setFont(font)
        self.textBrowser_2.setObjectName("textBrowser_2")
        self.verticalLayout_2.addWidget(self.textBrowser_2)
        self.textBrowser_3 = QtWidgets.QTextBrowser(self.widget_7)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textBrowser_3.sizePolicy().hasHeightForWidth())
        self.textBrowser_3.setSizePolicy(sizePolicy)
        self.textBrowser_3.setMinimumSize(QtCore.QSize(0, 30))
        self.textBrowser_3.setObjectName("textBrowser_3")
        self.verticalLayout_2.addWidget(self.textBrowser_3)
        self.verticalLayout_2.setStretch(0, 1)
        self.verticalLayout_2.setStretch(1, 10)
        self.horizontalLayout_4.addWidget(self.widget_7)
        self.horizontalLayout_4.setStretch(0, 2)
        self.verticalLayout.addWidget(self.widget_3)
        self.widget_4 = QtWidgets.QWidget(self.widget_2)
        self.widget_4.setObjectName("widget_4")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.widget_4)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.takePictureButton = QtWidgets.QToolButton(self.widget_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.takePictureButton.sizePolicy().hasHeightForWidth())
        self.takePictureButton.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Adobe 黑体 Std R")
        font.setPointSize(16)
        self.takePictureButton.setFont(font)
        self.takePictureButton.setObjectName("takePictureButton")
        self.horizontalLayout_5.addWidget(self.takePictureButton)
        self.skipButton = QtWidgets.QToolButton(self.widget_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.skipButton.sizePolicy().hasHeightForWidth())
        self.skipButton.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Adobe 黑体 Std R")
        font.setPointSize(16)
        self.skipButton.setFont(font)
        self.skipButton.setObjectName("skipButton")
        self.horizontalLayout_5.addWidget(self.skipButton)
        self.startDetectButton = QtWidgets.QToolButton(self.widget_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.startDetectButton.sizePolicy().hasHeightForWidth())
        self.startDetectButton.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Adobe 黑体 Std R")
        font.setPointSize(16)
        self.startDetectButton.setFont(font)
        self.startDetectButton.setObjectName("startDetectButton")
        self.horizontalLayout_5.addWidget(self.startDetectButton)
        self.horizontalLayout_5.setStretch(0, 1)
        self.horizontalLayout_5.setStretch(1, 1)
        self.horizontalLayout_5.setStretch(2, 2)
        self.verticalLayout.addWidget(self.widget_4)
        self.widget_5 = QtWidgets.QWidget(self.widget_2)
        self.widget_5.setObjectName("widget_5")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.widget_5)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.textBrowser_4 = QtWidgets.QTextBrowser(self.widget_5)
        self.textBrowser_4.setObjectName("textBrowser_4")
        self.horizontalLayout_6.addWidget(self.textBrowser_4)
        self.verticalLayout.addWidget(self.widget_5)
        self.verticalLayout.setStretch(0, 2)
        self.verticalLayout.setStretch(1, 1)
        self.verticalLayout.setStretch(2, 4)
        self.horizontalLayout.addWidget(self.widget_2)
        self.horizontalLayout.setStretch(0, 5)
        self.horizontalLayout.setStretch(1, 2)

        self.retranslateUi(PicturePage)
        self.stackedWidget.setCurrentIndex(-1)
        QtCore.QMetaObject.connectSlotsByName(PicturePage)

    def retranslateUi(self, PicturePage):
        _translate = QtCore.QCoreApplication.translate
        PicturePage.setWindowTitle(_translate("PicturePage", "PicturePage"))
        self.pushButton.setText(_translate("PicturePage", "缩略图"))
        self.textBrowser_2.setHtml(_translate("PicturePage", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'SimSun\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:9pt;\">产品工位：</span></p></body></html>"))
        self.textBrowser_3.setHtml(_translate("PicturePage", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'SimSun\'; font-size:6pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">当前任务：</span></p></body></html>"))
        self.takePictureButton.setText(_translate("PicturePage", "启动"))
        self.skipButton.setText(_translate("PicturePage", "拍照"))
        self.startDetectButton.setText(_translate("PicturePage", "开始检测"))
