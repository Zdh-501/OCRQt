# -*- coding: utf-8 -*-

# TestPage implementation generated from reading ui file 'test2.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_TestPage(object):
    def setupUi(self, TestPage):
        TestPage.setObjectName("TestPage")
        TestPage.resize(866, 574)
        self.label = QtWidgets.QLabel(TestPage)
        self.label.setGeometry(QtCore.QRect(170, 210, 54, 16))
        self.label.setObjectName("label")

        self.retranslateUi(TestPage)
        QtCore.QMetaObject.connectSlotsByName(TestPage)

    def retranslateUi(self, TestPage):
        _translate = QtCore.QCoreApplication.translate
        TestPage.setWindowTitle(_translate("TestPage", "TestPage"))
        self.label.setText(_translate("TestPage", "测试界面"))
