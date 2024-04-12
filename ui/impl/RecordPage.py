import os
import sys
import pyodbc
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt,QSize
from PyQt5.QtGui import QPixmap, QIcon, QImageReader, QFont, QImage
from PyQt5.QtWidgets import QTableWidgetItem, QCheckBox, QListWidgetItem, QMessageBox, QGraphicsPixmapItem, QGraphicsScene, QApplication
from pyqt5_plugins.examplebuttonplugin import QtGui

from ui.layout.UI_RecordPage import Ui_RecordPage
from SQL.dbFunction import dbConnect


class RecordPage(QtWidgets.QWidget, Ui_RecordPage):
    def __init__(self):
        super(RecordPage, self).__init__()
        self.setupUi(self)  # 从UI_RecordPage.py中加载UI定义

        # 初始化 QGraphicsScene
        self.scene = QGraphicsScene(self)
        self.graphicsView.setScene(self.scene)
        self.pixmapItem = None

        self.results_data = []  # 用于存储查询结果的全局变量

        self.tableWidget.setSortingEnabled(True)
        self.tableWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableWidget.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tableWidget.setColumnCount(4)  # 依据您的列数
        self.tableWidget.setHorizontalHeaderLabels(
            ['勾选框','任务标识符', '工单号', '批号'])
        # 使用关键字参数连接到数据库
        self.db = dbConnect()
        # 连接按钮信号
        self.pushButton_1.clicked.connect(self.query_records)

        self.pushButton_6.clicked.connect(self.delete_checked_items)
        # 连接全选复选框的状态改变信号
        self.checkBox.stateChanged.connect(self.toggleSelectAll)
        # 连接列表项点击信号
        self.tableWidget.cellClicked.connect(self.displayImage)

        self.pushButton_4.clicked.connect(lambda: self.scaleImage(1.25))  # 放大
        self.pushButton_3.clicked.connect(lambda: self.scaleImage(0.8))  # 缩小

        # 初始化dateTimeEdit控件
        self.dateTimeEdit_1.setDateTime(QtCore.QDateTime.currentDateTime().addDays(-30))  # 默认起始时间为30天前
        self.dateTimeEdit_2.setDateTime(QtCore.QDateTime.currentDateTime())  # 默认结束时间为当前时间

    def displayImage(self, row, column):
        # 获取保存的结果数据
        data = self.results_data[row]
        image_data = data[6]  # 假定IMAGE字段在结果中的索引为6

        try:
            if image_data:
                # 清除之前的图像
                self.scene.clear()

                # 分割字符串以处理可能存在的多张图片
                images_base64 = image_data.split(',')
                total_width = 0  # 用于累计所有图片的总宽度，以便并排显示

                # 遍历所有的Base64编码的图片
                for base64_str in images_base64:
                    # 对每张图像数据进行Base64解码并显示
                    image_bytes = QtCore.QByteArray.fromBase64(base64_str.encode())
                    image = QImage.fromData(image_bytes)
                    pixmap = QPixmap.fromImage(image)

                    # 创建QGraphicsPixmapItem对象并添加到场景中
                    pixmapItem = QGraphicsPixmapItem(pixmap)
                    pixmapItem.setPos(total_width, 0)  # 设置图片的位置
                    self.scene.addItem(pixmapItem)

                    total_width += pixmap.width()  # 更新总宽度

                # 调整视图以适应内容
                self.graphicsView.fitInView(self.scene.itemsBoundingRect(), Qt.KeepAspectRatio)
        except Exception as e:
            print(f"在 displayImage 方法中发生错误: {e}")

        self.displayProductInfo(row)

    def displayProductInfo(self,index):

        # 获取保存的结果数据
        data = self.results_data[index]
        task_identifier, sequence, order_no, batch_no, production_date, expiry_date, image_data, cwid, operationtime = data

        try:
            info = (f"任务标识符: {task_identifier}\n"
                    f"序号: {sequence}\n"
                    f"工单号: {order_no}\n"
                    f"批号: {batch_no}\n"
                    f"生产日期: {production_date}\n"
                    f"有效期至: {expiry_date}\n"
                    f"工作编号: {cwid}\n"
                    f"操作时间: {operationtime}\n")
            # 设置文本
            self.textBrowser.setText(info)

            # 设置label_4显示cwid和operationtime
            self.label_4.setText(f"{cwid}_{operationtime}")
        except Exception as e:
            print(f"在 displayProductInfo 方法中发生错误: {e}")

    def scaleImage(self, factor):
        if self.pixmapItem:
            currentScale = self.pixmapItem.scale()
            self.pixmapItem.setScale(currentScale * factor)

    def query_records(self):
        start_time = self.dateTimeEdit_1.dateTime().toString("yyyy-MM-dd HH:mm:ss")
        end_time = self.dateTimeEdit_2.dateTime().toString("yyyy-MM-dd HH:mm:ss")
        cwid_filter = self.lineEdit.text().strip()  # 使用 CWID 过滤

        try:
            with self.db.cursor() as cursor:
                query = """SELECT TASK_IDENTIFIER, SEQUENCE, ORDER_NO, BATCH_NO, PRODUCTION_DATE, 
                                EXPIRY_DATE, IMAGE, CWID, OPERATIONTIME 
                           FROM dbo.ResultTable 
                           WHERE OPERATIONTIME BETWEEN ? AND ?"""
                params = [start_time, end_time]

                if cwid_filter:  # 如果 CWID 过滤文本框内有内容
                    query += " AND CWID = ?"  # 添加 CWID 到 WHERE 条件
                    params.append(cwid_filter)

                cursor.execute(query, params)
                self.results_data = cursor.fetchall()
                self.tableWidget.setRowCount(0)  # 清空表格

                for row_index, row_data in enumerate(self.results_data):
                    self.tableWidget.insertRow(row_index)

                    # 创建一个包含复选框的QWidget
                    checkbox_widget = QtWidgets.QWidget()
                    checkbox_layout = QtWidgets.QHBoxLayout(checkbox_widget)
                    checkbox = QtWidgets.QCheckBox()
                    checkbox_layout.addWidget(checkbox)
                    checkbox_layout.setAlignment(QtCore.Qt.AlignCenter)
                    checkbox_layout.setContentsMargins(0, 0, 0, 0)
                    self.tableWidget.setCellWidget(row_index, 0, checkbox_widget)

                    # 为TASK_IDENTIFIER, ORDER_NO, BATCH_NO设置QTableWidgetItem
                    for col_index, data in enumerate([row_data[0], row_data[2], row_data[3]], start=1):
                        item = QtWidgets.QTableWidgetItem(str(data))
                        item.setTextAlignment(QtCore.Qt.AlignCenter)  # 设置文本居中
                        self.tableWidget.setItem(row_index, col_index, item)

                    self.tableWidget.setRowHeight(row_index, 40)  # 设置行高
        except Exception as e:
            QMessageBox.critical(self, "数据库错误", str(e))

    def convert_image_data(self, image_data):
        # 假设 IMAGE 字段包含的是Base64编码的图像数据
        if image_data is not None and image_data != '':
            # 对图像数据进行Base64解码
            image_bytes = QtCore.QByteArray.fromBase64(image_data.encode())
            image = QtGui.QImage.fromData(image_bytes)
            if image.isNull():
                QMessageBox.critical(self, "图像显示错误", "无法解析图像数据")
                return None
            return QPixmap.fromImage(image)
        return None

    def toggleSelectAll(self, state):
        for row in range(self.tableWidget.rowCount()):
            # 获取包含复选框的QWidget
            checkbox_widget = self.tableWidget.cellWidget(row, 0)
            # 确保获取到了QWidget
            if checkbox_widget:
                # 从布局中获取QCheckBox
                checkbox = checkbox_widget.layout().itemAt(0).widget()
                # 确保获取到的是QCheckBox，然后设置其状态
                if isinstance(checkbox, QtWidgets.QCheckBox):
                    checkbox.setChecked(state == Qt.Checked)

    def delete_checked_items(self):
        try:
            checked_rows = []
            with self.db.cursor() as cursor:
                for row in range(self.tableWidget.rowCount()):
                    # 获取包含复选框的QWidget
                    checkbox_widget = self.tableWidget.cellWidget(row, 0)
                    # 从布局中获取复选框
                    checkbox = checkbox_widget.layout().itemAt(0).widget()
                    if checkbox.isChecked():
                        checked_rows.append(row)

                if not checked_rows:
                    QMessageBox.information(self, "提示", "请勾选要删除的项")
                    return

                reply = QMessageBox.question(self, '确认删除', '您确定要删除勾选的项吗？',
                                             QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

                if reply == QMessageBox.Yes:
                    for row in sorted(checked_rows, reverse=True):
                        # 假设OPERATIONTIME字段是用于删除的标识符，并且它在self.results_data中的索引是8
                        operation_time = self.results_data[row][-1]  # 使用-1假设OPERATIONTIME在最后
                        query = "DELETE FROM dbo.ResultTable WHERE OPERATIONTIME = ?"
                        cursor.execute(query, (operation_time,))
                        self.db.commit()

                        # 从表中移除行
                        self.tableWidget.removeRow(row)
                        # 同步移除self.results_data中的数据
                        self.results_data.pop(row)

        except Exception as e:
            QMessageBox.critical(self, "数据库错误", str(e))
            self.db.rollback()

    def perform_deletion(self, selected_items):
        try:
            with self.db.cursor() as cursor:
                for item in selected_items:
                    image_path = item.data(Qt.UserRole)  # 获取存储的图片路径
                    query = f"DELETE FROM products WHERE image_path = '{image_path}'"
                    cursor.execute(query)
                    self.db.commit()

                    # 从列表中移除项
                    row = self.listWidget.row(item)
                    self.listWidget.takeItem(row)

        except Exception as e:
            QMessageBox.critical(self, "数据库错误", str(e))
            self.db.rollback()

    # 确保在退出时关闭数据库连接
    def closeEvent(self, event):
        self.db.close()
        super(RecordPage, self).closeEvent(event)

#创建应用实例和窗口，然后运行
# app = QApplication(sys.argv)
# window = RecordPage()
# window.showMaximized()
# sys.exit(app.exec_())

