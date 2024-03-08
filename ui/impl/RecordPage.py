import os
import sys
import pyodbc
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt,QSize
from PyQt5.QtGui import QPixmap, QIcon, QImageReader, QFont, QImage
from PyQt5.QtWidgets import QListWidgetItem, QMessageBox, QGraphicsPixmapItem, QGraphicsScene, QApplication
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

        # 设置 listWidget 的图标尺寸
        self.listWidget.setIconSize(QSize(100, 100))  # 将图标尺寸设置为 100x100

        # 使用关键字参数连接到数据库
        self.db = dbConnect()
        # 连接按钮信号
        self.pushButton_1.clicked.connect(self.query_records)
        self.pushButton_2.clicked.connect(lambda: self.sort_records(True))
        self.pushButton_5.clicked.connect(lambda: self.sort_records(False))
        self.pushButton_6.clicked.connect(self.delete_checked_items)
        # 连接全选复选框的状态改变信号
        self.checkBox.stateChanged.connect(self.toggleSelectAll)
        # 连接列表项点击信号
        self.listWidget.itemClicked.connect(self.displayImage)
        self.pushButton_4.clicked.connect(lambda: self.scaleImage(1.25))  # 放大
        self.pushButton_3.clicked.connect(lambda: self.scaleImage(0.8))  # 缩小

        # 初始化dateTimeEdit控件
        self.dateTimeEdit_1.setDateTime(QtCore.QDateTime.currentDateTime().addDays(-30))  # 默认起始时间为30天前
        self.dateTimeEdit_2.setDateTime(QtCore.QDateTime.currentDateTime())  # 默认结束时间为当前时间

    def displayImage(self, item):
        # 获取选中项的索引
        index = self.listWidget.row(item)
        # 获取保存的结果数据
        data = self.results_data[index]
        image_data = data[6]  # 假定IMAGE字段在结果中的索引为6

        try:
            if image_data:
                # 对图像数据进行Base64解码并显示
                image_bytes = QtCore.QByteArray.fromBase64(image_data.encode())
                image = QImage.fromData(image_bytes)
                pixmap = QPixmap.fromImage(image)

                self.scene.clear()
                self.pixmapItem = QGraphicsPixmapItem(pixmap)
                self.scene.addItem(self.pixmapItem)
                self.graphicsView.fitInView(self.pixmapItem, Qt.KeepAspectRatio)
        except Exception as e:
            print(f"在 displayImage 方法中发生错误: {e}")
        self.displayProductInfo()

    def displayProductInfo(self):
        # 获取最后一次点击的项目的索引
        index = self.listWidget.currentRow()
        # 获取保存的结果数据
        data = self.results_data[index]
        task_identifier, sequence, order_no, batch_no, production_date, expiry_date, image_data, cwid, operationtime = data

        try:
            info = (f"任务标识符: {task_identifier}\n"
                    f"序列: {sequence}\n"
                    f"订单号: {order_no}\n"
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
        batch_no_filter = self.lineEdit.text().strip()  # 更改为使用批号过滤

        try:
            with self.db.cursor() as cursor:
                # 构建查询语句以选择所有字段
                query = """SELECT TASK_IDENTIFIER, SEQUENCE, ORDER_NO, BATCH_NO, PRODUCTION_DATE, 
                                EXPIRY_DATE, IMAGE, CWID, OPERATIONTIME 
                           FROM dbo.ResultTable 
                           WHERE OPERATIONTIME BETWEEN ? AND ?"""
                params = [start_time, end_time]

                # 如果有输入批号，则添加筛选条件
                if batch_no_filter:
                    query += " AND BATCH_NO = ?"
                    params.append(batch_no_filter)

                # 执行查询
                cursor.execute(query, params)
                self.results_data = cursor.fetchall()
                self.listWidget.clear()  # 清空当前列表

                for row in self.results_data:
                    task_identifier, sequence, order_no, batch_no, production_date, \
                        expiry_date, image_data, cwid, operationtime = row

                    # 解析 IMAGE 字段数据
                    pixmap = self.convert_image_data(image_data)
                    if pixmap is None:  # 如果解析失败，则跳过当前项
                        continue

                    icon = QIcon(pixmap.scaled(128, 128, Qt.KeepAspectRatio, Qt.SmoothTransformation))
                    item_text = f"{task_identifier} ({order_no}) - {batch_no}"
                    item = QListWidgetItem(icon, item_text)
                    self.listWidget.addItem(item)

                    item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
                    item.setCheckState(Qt.Unchecked)
                    self.listWidget.addItem(item)
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
        for i in range(self.listWidget.count()):
            item = self.listWidget.item(i)
            item.setCheckState(Qt.Checked if state == Qt.Checked else Qt.Unchecked)
    def sort_records(self, ascending):
        self.listWidget.sortItems(QtCore.Qt.AscendingOrder if ascending else QtCore.Qt.DescendingOrder)

    def delete_checked_items(self):
        # 检查是否有勾选项
        has_checked_items = any(self.listWidget.item(i).checkState() == Qt.Checked
                                for i in range(self.listWidget.count()))

        if not has_checked_items:
            QMessageBox.information(self, "提示", "请勾选要删除的项")
            return
        else:
            # 弹出确认对话框
            reply = QMessageBox.question(self, '确认删除', '您确定要删除勾选的项吗？',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

            if reply == QMessageBox.Yes:
                try:
                    with self.db.cursor() as cursor:
                        for i in range(self.listWidget.count() - 1, -1, -1):  # 倒序遍历，避免索引问题
                            item = self.listWidget.item(i)
                            if item.checkState() == Qt.Checked:
                                image_path = item.data(Qt.UserRole)
                                query = "DELETE FROM products WHERE image_path = %s"
                                cursor.execute(query, (image_path,))  # 使用参数化查询
                                self.db.commit()

                                # 从列表中移除项
                                self.listWidget.takeItem(i)

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

