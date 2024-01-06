# -*- coding: utf-8 -*-

# ModelMainPage implementation generated from reading ui file 'UI_ModelMainPage.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QFont


class Ui_ModelMainPage(object):
    def setupUi(self, ModelMainPage):
        ModelMainPage.setObjectName("ModelMainPage")
        ModelMainPage.resize(1170, 784)
        self.verticalLayout = QtWidgets.QVBoxLayout(ModelMainPage)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushButton_1 = QtWidgets.QPushButton(ModelMainPage)
        self.pushButton_1.setMinimumSize(QtCore.QSize(50, 40))
        self.pushButton_1.setObjectName("pushButton_1")
        self.horizontalLayout.addWidget(self.pushButton_1)
        self.pushButton_2 = QtWidgets.QPushButton(ModelMainPage)
        self.pushButton_2.setMinimumSize(QtCore.QSize(50, 40))
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout.addWidget(self.pushButton_2)
        self.pushButton_3 = QtWidgets.QPushButton(ModelMainPage)
        self.pushButton_3.setMinimumSize(QtCore.QSize(50, 40))
        self.pushButton_3.setObjectName("pushButton_3")
        self.horizontalLayout.addWidget(self.pushButton_3)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.horizontalLayout.setStretch(0, 5)
        self.horizontalLayout.setStretch(1, 1)
        self.horizontalLayout.setStretch(2, 1)
        self.horizontalLayout.setStretch(3, 1)
        self.horizontalLayout.setStretch(4, 5)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.stackedWidget = QtWidgets.QStackedWidget(ModelMainPage)
        self.stackedWidget.setObjectName("stackedWidget")
        self.verticalLayout.addWidget(self.stackedWidget)

        self.retranslateUi(ModelMainPage)
        QtCore.QMetaObject.connectSlotsByName(ModelMainPage)

    def retranslateUi(self, ModelMainPage):
        # 创建字体对象并设置大小
        font = QFont()
        font.setPointSize(16)  # 设置字体大小为16点
        _translate = QtCore.QCoreApplication.translate
        ModelMainPage.setWindowTitle(_translate("ModelMainPage", "ModelMainPage"))
        self.pushButton_1.setText(_translate("ModelMainPage", "数据集管理"))
        self.pushButton_2.setText(_translate("ModelMainPage", "模型训练"))
        self.pushButton_3.setText(_translate("ModelMainPage", "模型管理"))
        self.pushButton_1.setFont(font)
        self.pushButton_2.setFont(font)
        self.pushButton_3.setFont(font)