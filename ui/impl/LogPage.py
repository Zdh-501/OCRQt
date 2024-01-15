import sys

from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QApplication,QTableWidgetItem, QHeaderView



from SQL.dbFunction import *
from ui.layout.UI_LogPage import Ui_LogPage

class LogPage(QtWidgets.QWidget,Ui_LogPage):
    def __init__(self):
        super(LogPage, self).__init__()
        self.setupUi(self)  # 从UI_DataCollectPage.py中加载UI定义
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.loadErrorLogs()  # 调用方法来加载错误日志



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
            row_height = 50  # 将行高设置为40像素

            # 遍历并添加数据到tableWidget中
            for row_number, row_data in enumerate(rows):
                self.tableWidget.setRowHeight(row_number, row_height)  # 设置行高

                for column_number, data in enumerate(row_data):
                    item = QtWidgets.QTableWidgetItem(str(data))
                    item.setFont(font)  # 设置字体
                    self.tableWidget.setItem(row_number, column_number, item)
            # 设置列宽以适应内容
            self.tableWidget.resizeColumnsToContents()

        except pyodbc.Error as e:
                print("数据库错误: ", e)
        finally:
            if connection:
                connection.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = LogPage()
    mainWindow.show()
    app.exec_()