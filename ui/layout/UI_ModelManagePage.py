# -*- coding: utf-8 -*-

# ModelManagePage implementation generated from reading ui file 'UI_ModelManagePage.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ModelManagePage(object):
    def setupUi(self, ModelManagePage):
        ModelManagePage.setObjectName("ModelManagePage")
        ModelManagePage.resize(633, 444)
        self.verticalLayout = QtWidgets.QVBoxLayout(ModelManagePage)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tableWidget = QtWidgets.QTableWidget(ModelManagePage)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.tableWidget.setFont(font)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.tableWidget.horizontalHeader().setStretchLastSection(False)
        self.verticalLayout.addWidget(self.tableWidget)

        self.retranslateUi(ModelManagePage)
        QtCore.QMetaObject.connectSlotsByName(ModelManagePage)

    def retranslateUi(self, ModelManagePage):
        _translate = QtCore.QCoreApplication.translate
        ModelManagePage.setWindowTitle(_translate("ModelManagePage", "ModelManagePage"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ModelManagePage = QtWidgets.QWidget()
    ui = Ui_ModelManagePage()
    ui.setupUi(ModelManagePage)
    ModelManagePage.show()
    sys.exit(app.exec_())
