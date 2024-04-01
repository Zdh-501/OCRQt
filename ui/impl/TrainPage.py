import sys
import os
import subprocess
from datetime import datetime
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QTableWidgetItem, QApplication,QFileDialog,QMessageBox
from PyQt5 import QtCore, QtWidgets

from ui.layout.UI_TrainPage import Ui_TrainPage
from ui.impl.myThread import *
from SQL.dbFunction import *
class TrainPage(QtWidgets.QWidget,Ui_TrainPage):
    # 定义一个没有参数的信号
    trainStrat = pyqtSignal()
    # 定义一个带有一个bool和一个str参数的信号
    trainingFinished = pyqtSignal(bool, str)
    def __init__(self, user_cwid, user_name):
        super(TrainPage, self).__init__()
        self.setupUi(self)  # 从UI_TaskPage.py中加载UI定义
        self.trainButton.clicked.connect(self.on_train_button_clicked)
        self.dataButton.clicked.connect(self.select_data_path)
        self.preModelButton.clicked.connect(self.select_pre_model_path)
        self.saveButton.clicked.connect(self.select_save_path)

        self.user_cwid = user_cwid
        self.user_name = user_name
        self.training_start_time = None  # 添加属性来存储训练开始时间
    def select_data_path(self):
        # 打开文件选择对话框
        data_path = QFileDialog.getExistingDirectory(self, "选择数据集目录")
        # 将选定的路径显示在dataSetEdit输入框中
        if data_path:  # 如果用户选择了路径
            self.dataSetEdit.setText(data_path.replace('/', '\\'))  # 在Windows上使用反斜杠

    def select_pre_model_path(self):
        # 打开文件选择对话框，选择文件而不是文件夹
        pre_model_path, _ = QFileDialog.getOpenFileName(self, "选择预训练模型文件", "",
                                                        "模型参数文件 (*.pdparams);;所有文件 (*)")
        # 将选定的路径显示在preEdit输入框中
        if pre_model_path:  # 如果用户选择了文件
            self.preEdit.setText(pre_model_path.replace('/', '\\'))  # 在Windows上使用反斜杠

    def select_save_path(self):
        # 打开文件选择对话框
        save_path = QFileDialog.getExistingDirectory(self, "选择保存模型的目录")
        # 将选定的路径显示在saveEdit输入框中
        if save_path:  # 如果用户选择了路径
            self.saveEdit.setText(save_path.replace('/', '\\'))  # 在Windows上使用反斜杠

    def check_all_fields_filled(self):
        # 检查所有需要的输入框是否已填写
        if not self.dataSetEdit.text().strip():
            QMessageBox.warning(self, '输入错误', '请指定数据集路径。')
            return
        if not self.preEdit.text().strip():
            QMessageBox.warning(self, '输入错误', '请指定预训练模型文件。')
            return
        if not self.saveEdit.text().strip():
            QMessageBox.warning(self, '输入错误', '请指定模型保存路径。')
            return
        if not self.nameEdit.text().strip():
            QMessageBox.warning(self, '输入错误', '请指定训练模型的名称。')
            return
        if not self.epochEdit.text().strip():
            QMessageBox.warning(self, '输入错误', '请指定epoch次数。')
            return
        if not self.batchEdit.text().strip():
            QMessageBox.warning(self, '输入错误', '请指定batch size。')
            return
        return True

    def infer_model_type_from_pretrained_name(self, pretrained_path):
        # 假设预训练模型文件名中包含'model_type'关键字
        filename = os.path.basename(pretrained_path)
        if 'det' in filename:
            return 'det'
        elif 'rec' in filename:
            return 'rec'
        else:
            return None

    def on_train_button_clicked(self):
        # 检查模型类型选择
        if not self.detBox.isChecked() and not self.recBox.isChecked():
            QMessageBox.warning(self, '错误', '请先勾选要训练的模型类型。')
            return
        elif self.detBox.isChecked() and self.recBox.isChecked():
            QMessageBox.warning(self, '错误', '只能选择一种模型类型进行训练。')
            return
        else:
            model_type = 'det' if self.detBox.isChecked() else 'rec'

        if not self.check_all_fields_filled():
            return

        # 获取UI组件中的值
        dataset_root_path = self.dataSetEdit.text().replace('/', '\\')  # 替换为Windows风格的路径
        pre_model_path = self.preEdit.text().replace('/', '\\')  # 预训练模型路径输入框
        save_path = self.saveEdit.text().replace('/', '\\')  # 模型保存路径输入框
        epochs = self.epochEdit.text()  # Epoch次数输入框
        batch_size = self.batchEdit.text()  # Batch size输入框
        det_path = os.path.join(dataset_root_path, "det")  # 构造det数据集的路径
        rec_path = os.path.join(dataset_root_path, "rec")  # 构造rec数据集的路径


        print(f"Dataset root path: {dataset_root_path}")
        # 构建数据集划分命令

        divide_dataset_cmd = f"paddle\\python.exe .\\PaddleOCR\\PPOCRLabel\\gen_ocr_train_val_test.py --trainValTestRatio 6:2:2 --datasetRootPath \"{dataset_root_path}\" --detRootPath \"{det_path}\" --recRootPath \"{rec_path}\""


        # 根据模型类型构建相应的训练命令
        if model_type == 'det':
            train_cmd = self.construct_train_command('det', dataset_root_path, pre_model_path, save_path, epochs,
                                                     batch_size)
        else:
            train_cmd = self.construct_train_command('rec', dataset_root_path, pre_model_path, save_path, epochs,
                                                     batch_size)

        # 使用子线程同时执行划分数据集和训练命令
        self.training_thread = TrainingThread(divide_dataset_cmd, train_cmd)
        self.training_thread.trainingCompleted.connect(self.on_training_completed)
        self.training_thread.start()
        self.insert_model_info_to_database()
        #todo 添加上传数据库功能

    def insert_model_info_to_database(self):
        # 连接数据库
        connection = dbConnect()
        cursor = connection.cursor()

        # 准备要插入的数据
        model_name = self.nameEdit.text()
        pre_model_name = self.preEdit.text().replace('/', '\\')  # Windows路径风格
        remarks = self.infoTextEdit.toPlainText()  # 如果是QTextEdit，使用toPlainText获取文本
        storage_path = self.saveEdit.text().replace('/', '\\')
        status = "进行中"
        cwid = self.user_cwid
        training_start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # 格式化当前时间
        self.training_start_time = training_start_time
        # 构建SQL插入命令
        insert_query = """
               INSERT INTO ModelInformation 
               (ModelName, PretrainedModelName, Remarks, StoragePath, Status, CWID, UserName, TrainingStartTime)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)
           """

        # 执行插入命令
        try:
            cursor.execute(insert_query, (
            model_name, pre_model_name, remarks, storage_path, status, cwid, self.user_name, training_start_time))
            connection.commit()
            print("Model information inserted successfully.")
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            cursor.close()
            connection.close()
        # 数据插入完成后，发射信号
        self.trainStrat.emit()
    def construct_train_command(self, model_type, dataset_root_path, pre_model_path, save_path, epochs, batch_size):
        if model_type == 'det':
            config_file = ".\\PaddleOCR\\configs\\det\\det_mv3_db.yml"
            model_dir = "det"
        elif model_type == 'rec':
            config_file = ".\\PaddleOCR\\configs\\rec\\PP-OCRv3\\ch_PP-OCRv3_rec_distillation.yml"
            model_dir = "rec"

        train_cmd = (
            f"paddle\\python.exe .\\PaddleOCR\\tools\\train.py -c {config_file} "
            f"-o Global.pretrained_model=\"{pre_model_path}\" "
            f"Global.save_model_dir=\"{save_path}\\{model_dir}\" "
            f"Global.epoch_num={epochs} "
            f"Train.loader.batch_size_per_card={batch_size} "
            f"Eval.loader.batch_size_per_card={batch_size} "
            f"Train.dataset.data_dir=\"{dataset_root_path}\\{model_dir}\\train\" "
            f"Train.dataset.label_file_list=\"['{dataset_root_path}\\{model_dir}\\train.txt']\" "
            f"Eval.dataset.data_dir=\"{dataset_root_path}\\{model_dir}\\val\" "
            f"Eval.dataset.label_file_list=\"['{dataset_root_path}\\{model_dir}\\val.txt']\""
        )

        return train_cmd

    def on_training_completed(self, success, message):
        if success:
            QMessageBox.information(self, "训练完成", message)
            self.trainingFinished.emit(success, self.training_start_time)
        else:
            QMessageBox.critical(self, "训练失败", message)
        # 发射训练完成的信号，不再需要model_name，只需要传递训练开始时间

# if __name__ == '__main__':
# app = QApplication(sys.argv)
# mainWindow = TrainPage()
# mainWindow.show()
# app.exec_()