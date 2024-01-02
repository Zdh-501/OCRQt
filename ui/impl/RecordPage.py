import os
import sys
import pyodbc
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt,QSize
from PyQt5.QtGui import QPixmap, QIcon, QImageReader, QFont
from PyQt5.QtWidgets import QListWidgetItem, QMessageBox, QGraphicsPixmapItem, QGraphicsScene, QApplication
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
        try:
            # 从 UserRole 提取信息
            item_data = item.data(Qt.UserRole)
            image_path = item_data['TestResultImagePath']

            product_name = item_data['ProductName']

            product_id = item_data['ProductCode']


            # 显示图片
            pixmap = self.load_image(image_path)
            if not pixmap.isNull():
                self.scene.clear()
                self.pixmapItem = QGraphicsPixmapItem(pixmap)
                self.scene.addItem(self.pixmapItem)
                self.graphicsView.fitInView(self.pixmapItem, Qt.KeepAspectRatio)
        except Exception as e:
            print(f"在 displayImage 方法中发生错误: {e}")

        # 显示产品信息
        self.displayProductInfo(product_id)


    def displayProductInfo(self, product_id):
        try:
            # 假设 dbConnect 是一个返回新的数据库连接的函数

            connection = dbConnect()
            with connection.cursor() as cursor:
                # 根据 product_id 查询数据
                query = "SELECT * FROM ProductDetails WHERE ProductCode = ?"
                cursor.execute(query, (product_id,))
                result = cursor.fetchone()
                # cursor.fetchone() 返回的默认结果类型是元组，每个元素对应 SQL 查询中选择的列
                if result:
                    # 格式化并显示全部产品信息
                    info = (f"产品编码: {result[0]}\n"
                            f"产品名称: {result[1]}\n"
                            f"任务序号: {result[2]}\n"
                            f"生产批号: {result[3]}\n"
                            f"生产日期: {result[4]}\n"
                            f"有效期至: {result[5]}\n"
                            f"检测结果: {result[6]}\n"
                            f"完成时间: {result[7]}")
                    # 设置字体大小
                    font = QFont()
                    font.setPointSize(12)  # 设置字体大小为 12，您可以根据需要调整这个值

                    self.textBrowser.setFont(font)
                    self.textBrowser.setText(info)
                    self.textBrowser.setText(info)
                    self.label_4.setText(result[2])  # 产品名称
        except Exception as e:
            print(f"数据库查询错误: {e}")
        finally:
            connection.close()

    def scaleImage(self, factor):
        if self.pixmapItem:
            currentScale = self.pixmapItem.scale()
            self.pixmapItem.setScale(currentScale * factor)


    def load_image(self, image_path):

        # 检查文件是否存在
        if not os.path.exists(image_path):
            QMessageBox.critical(self, "加载图片错误", "文件不存在: " + image_path)
            return None

        reader = QImageReader(image_path)
        image = reader.read()
        if image.isNull():
            error = reader.errorString()
            QMessageBox.critical(self, "加载图片错误", f"无法加载图片: {error}")
            return None
        return QPixmap.fromImage(image)

    def query_records(self):
        start_time = self.dateTimeEdit_1.dateTime().toString("yyyy-MM-dd HH:mm:ss")
        end_time = self.dateTimeEdit_2.dateTime().toString("yyyy-MM-dd HH:mm:ss")
        batch_number_filter = self.lineEdit.text().strip()

        try:
            with self.db.cursor() as cursor:
                # 构建基础查询语句
                query = "SELECT TestResultImagePath, ProductName, ProductCode FROM ProductDetails WHERE ProductionDate BETWEEN ? AND ?"
                params = [start_time, end_time]

                # 如果 self.lineEdit 中有输入内容，则添加额外的筛选条件
                if batch_number_filter:
                    query += " AND BatchNumber = ?"
                    params.append(batch_number_filter)

                # 执行查询
                cursor.execute(query, params)
                results = cursor.fetchall()
                self.listWidget.clear()  # 清空当前列表

                for row in results:
                    test_result_image_path, product_name, product_code = row
                    # 使用 load_image 方法加载图片

                    pixmap = self.load_image(test_result_image_path)
                    if pixmap is None:  # 如果加载失败，则跳过当前项
                        continue

                    icon = QIcon(pixmap.scaled(128, 128, Qt.KeepAspectRatio, Qt.SmoothTransformation))

                    # 创建带有图标和文本的 QListWidgetItem
                    item_text = f"{product_name} ({product_code}) {test_result_image_path}"
                    item = QListWidgetItem(icon, item_text)
                    item.setData(Qt.UserRole,
                                 {"TestResultImagePath": test_result_image_path, "ProductName": product_name,
                                  "ProductCode": product_code})
                    item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
                    item.setCheckState(Qt.Unchecked)
                    self.listWidget.addItem(item)
        except Exception as e:
            QMessageBox.critical(self, "数据库错误", str(e))

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

