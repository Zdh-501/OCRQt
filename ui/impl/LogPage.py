import sys

from PyQt5 import QtWidgets, QtGui


from SQL.dbFunction import *
from ui.impl.LoginDialog import *

from SQL.dbFunction import *
from ui.layout.UI_LogPage import Ui_LogPage

class LogPage(QtWidgets.QWidget,Ui_LogPage):
    def __init__(self):
        super(LogPage, self).__init__()
        self.setupUi(self)  # 从UI_DataCollectPage.py中加载UI定义
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        # 启用表格排序功能
        self.tableWidget.setSortingEnabled(True)
        self.loadErrorLogs()  # 调用方法来加载错误日志
        self.clearButton.clicked.connect(self.clearData)
        self.flashButton.clicked.connect(self.flashData)

    def loadErrorLogs(self):
        try:
            # 连接到数据库
            connection = dbConnect()
            cursor = connection.cursor()

            # 查询ErrorLog表中的所有数据
            cursor.execute("SELECT OccurrenceTime, ErrorMessage FROM ErrorLog")
            rows = cursor.fetchall()

            # 设置tableWidget的行数
            self.tableWidget.setRowCount(len(rows))
            # 设置字体
            font = QtGui.QFont()
            font.setPointSize(13)  # 设置字体大小为13

            # 设置行高
            row_height = 50  # 将行高设置为50像素

            # 遍历并添加数据到tableWidget中
            for row_number, row_data in enumerate(rows):
                self.tableWidget.setRowHeight(row_number, row_height)  # 设置行高

                for column_number, data in enumerate(row_data):
                    item = QtWidgets.QTableWidgetItem(str(data))
                    item.setFont(font)  # 设置字体
                    # 设置单元格不可编辑
                    item.setFlags(item.flags() & ~Qt.ItemIsEditable)

                    # 如果是第一列，设置文本居中对齐
                    if column_number == 0:
                        item.setTextAlignment(Qt.AlignCenter)
                    self.tableWidget.setItem(row_number, column_number, item)
            # 设置列宽以适应内容
            self.tableWidget.resizeColumnsToContents()
            self.tableWidget.setColumnWidth(0, 450)  # 设置第一列的宽度为 450 像素

        except pyodbc.Error as e:
                print("数据库错误: ", e)
        finally:
            if connection:
                connection.close()

    def clearData(self):
        login_dialog = LoginDialog(self)
        if login_dialog.exec_() == QDialog.Accepted:
            # 登录成功，清空tableWidget中的数据
            self.tableWidget.clearContents()
            self.tableWidget.setRowCount(0)
    def flashData(self):
        self.loadErrorLogs()
if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = LogPage()
    mainWindow.show()
    app.exec_()