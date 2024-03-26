import os
import sys
from pathlib import Path
import imageio
import requests
from PyQt5.QtCore import QThread, pyqtSignal, QBuffer, QIODevice
import numpy as np
from mphdcpy import mphdc
import cv2
import paddleocr
from threading import Condition
from PIL import Image
from io import BytesIO
from paddleocr import PaddleOCR
import subprocess
import ctypes as ct
import time
import base64
import traceback
from datetime import datetime

from SQL.dbFunction import *
from ui.impl.resClient import *

# 定义图像捕获线程类
class CameraWorker(QThread):
    image_captured = pyqtSignal(np.ndarray)

    def __init__(self, camera):
        super().__init__()
        self.camera = camera
        self._is_running = True
        self._is_paused = False
        self._pause_condition = Condition()
        self.active_channels = ['nx', 'ny', 'nz']  # 添加这行来存储当前激活的通道
    def run(self):
        while self._is_running:
            # 检查暂停标志
            with self._pause_condition:
                while self._is_paused:
                    self._pause_condition.wait()
            state = mphdc.GetCameraState(self.camera)
            if state == mphdc.DeviceStateType.StandBy:
                res, data = mphdc.SnapCamera(self.camera, 1000)
                if res:
                    imgs, n, channels = mphdc.Nppc_Create(data)
                    if n > 0:
                        if 'nx' in self.active_channels and 'ny' in self.active_channels and 'nz' in self.active_channels:

                            # 合并 nx, ny, nz 通道
                            nx_channel = imgs[channels.index(mphdc.ImageContentType.Photometric_Nx),:,:]
                            ny_channel = imgs[channels.index(mphdc.ImageContentType.Photometric_Ny),:,:]
                            nz_channel = imgs[channels.index(mphdc.ImageContentType.Photometric_Nz),:,:]
                            merged_image = cv2.merge([nx_channel, ny_channel, nz_channel])

                            # 首先进行上下颠倒
                            nx_channel_flipped_vertical = cv2.flip(nx_channel, 0)  # 上下颠倒，左右不变
                            ny_channel_flipped_vertical = cv2.flip(ny_channel, 0)  # 上下颠倒，左右不变
                            nz_channel_flipped_vertical = cv2.flip(nz_channel, 0)  # 上下颠倒，左右不变

                            # 然后进行左右镜像反转
                            nx_channel_flipped_horizontal = cv2.flip(nx_channel_flipped_vertical, 1)  # 左右镜像反转
                            ny_channel_flipped_horizontal = cv2.flip(ny_channel_flipped_vertical, 1)  # 左右镜像反转
                            nz_channel_flipped_horizontal = cv2.flip(nz_channel_flipped_vertical, 1)  # 左右镜像反转

                            # 合并翻转后的通道
                            merged_image_flipped = cv2.merge([
                                nx_channel_flipped_horizontal,
                                ny_channel_flipped_horizontal,
                                nz_channel_flipped_horizontal
                            ])
                        elif 'kd' in self.active_channels:

                            kd_channel = imgs[channels.index(mphdc.ImageContentType.Photometric_Kd), :, :]
                            merged_image = cv2.merge([kd_channel, kd_channel, kd_channel])
                            # 首先进行上下颠倒
                            kd_channel_flipped_vertical = cv2.flip(kd_channel, 0)  # 上下颠倒，左右不变
                            # 然后进行左右镜像反转
                            kd_channel_flipped_horizontal = cv2.flip(kd_channel_flipped_vertical, 1)  # 左右镜像反转
                            # 合并翻转后的通道
                            merged_image_flipped = cv2.merge([
                                kd_channel_flipped_horizontal,
                                kd_channel_flipped_horizontal,
                                kd_channel_flipped_horizontal
                            ])
                        self.image_captured.emit(merged_image_flipped)

    def is_paused(self):
        return self._is_paused

    def pause(self):
        with self._pause_condition:
            self._is_paused = True

    def resume(self):
        with self._pause_condition:
            self._is_paused = False
            self._pause_condition.notify()
    def stop(self):
        self._is_running = False

# OCR检测子线程 ocr_instance  self.ocr = ocr_instance  # 使用传入的 PaddleOCR 实例
class OcrThread(QThread):
    finished = pyqtSignal(object)  # 完成信号，传递检测结果

    def __init__(self, Ocr, images, det_model_dir,rec_model_dir,det_db_unclip_ratio, parent=None):
        super().__init__(parent)
        self.images = images  # NumPy图像数组列表
        self.Ocr = Ocr  # 直接使用传入的PaddleOCR实例
        print('Ocr', paddleocr.__version__)

    def run(self):
        results = []
        for i, image_np in enumerate(self.images):
            # 打印原始图像大小
            print(f"Original image {i} size: {image_np.shape}")

            # 调整图像大小
            # 假设我们想要将图像的最长边限制为960像素
            # scale_factor = 960 / max(image_np.shape[:2])
            # width = int(image_np.shape[1] * scale_factor)
            # height = int(image_np.shape[0] * scale_factor)
            # dim = (width, height)
            # resized_image = cv2.resize(image_np, dim, interpolation=cv2.INTER_AREA)
            #
            # # 打印调整后的图像大小
            # print(f"Resized image {i} size: {resized_image.shape}")


            result = self.Ocr.ocr(image_np, cls=True)
            results.append((i, result))


        self.finished.emit(results)  # 发送完成信号，附带检测结果
class DatabaseOperationThread(QThread):
    def __init__(self, task_key, captured_images, user_cwid, task_index, dates, batch_numbers, parent=None):
        super(DatabaseOperationThread, self).__init__(parent)
        self.task_key = task_key
        self.captured_images = captured_images
        self.dates = dates
        self.batch_numbers = batch_numbers
        self.task_index = task_index
        self.user_cwid = user_cwid

    def run(self):
        error = ""
        # 连接数据库
        connection = dbConnect()
        cursor = connection.cursor()

        # 构造查询语句
        # 假设 self.task_identifier 已经定义并且包含了要查询的任务标识符的值
        query = """SELECT ORDER_NO, TASK_IDENTIFIER
                           FROM TaskInformation
                           WHERE  TASK_KEY = ?"""
        try:
            # 执行查询操作
            print("测试，", self.task_key)
            cursor.execute(query, (self.task_key,))
            # 获取查询结果的第一条记录
            result = cursor.fetchone()  # 假设每个 TASK_IDENTIFIER 唯一
            # 检查是否找到了结果
            if result:
                # 将查询结果存储在类的属性中
                self.order_no, self.task_identifier = result
                print("测试", self.task_identifier)
                self.operation_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                self.batch_no = self.batch_numbers[0]
                if len(self.dates) == 1:
                    self.expiry_date = self.dates[0]
                    self.production_date = ''  # 或者使用 '' 表示空字符串，根据您的需要
                else:
                    # 将日期字符串转换为日期对象的函数
                    def convert_to_date(date_str):
                        try:
                            return datetime.strptime(date_str, '%Y-%m-%d')
                        except ValueError:
                            return datetime.strptime(date_str, '%d-%m-%Y')

                    # 转换两个日期
                    date1 = convert_to_date(self.dates[0])
                    date2 = convert_to_date(self.dates[1])

                    # 比较并赋值
                    if date1 < date2:
                        self.production_date = self.dates[0]
                        self.expiry_date = self.dates[1]
                    else:
                        self.production_date = self.dates[1]
                        self.expiry_date = self.dates[0]
                # 假设 self.captured_images 是包含多个 NumPy 图像数组的列表
                self.images_base64 = []
                for image_np in self.captured_images:
                    # 将 NumPy 图像数组编码为 JPEG 格式的字节流
                    retval, buffer = cv2.imencode('.jpg', image_np)
                    if retval:
                        # 将字节流编码为 Base64 字符串
                        image_base64 = base64.b64encode(buffer).decode('utf-8')
                        self.images_base64.append(image_base64)

                # 将 Base64 字符串列表连接成一个长字符串，以逗号分隔
                self.images_str = ','.join(self.images_base64)

                result = Result(
                    task_identifier=self.task_identifier,
                    batch_no=self.batch_no,
                    task_key=self.task_key,
                    sequence=self.task_index,
                    order_no=self.order_no,
                    production_date=self.production_date,
                    expiry_date=self.expiry_date,
                    image=self.images_str,
                    cwid=self.user_cwid,
                    operation_time=self.operation_time
                )
                send_result_to_bes(result)
            else:
                error="没有找到匹配的任务信息。"
        except Exception as e:
            error=f" 类型: {type(e)}, 错误信息: {e}"
        finally:
            # 关闭数据库连接
            cursor.close()
            connection.close()

        # 连接数据库
        connection = dbConnect()
        cursor = connection.cursor()

        # 将结果存入结果数据表
        try:
            # 先执行之前的查询操作，然后...

            # 插入数据到 ResultTable
            insert_query = """
                    INSERT INTO ResultTable (TASK_IDENTIFIER, BATCH_NO, SEQUENCE, ORDER_NO, PRODUCTION_DATE, EXPIRY_DATE, IMAGE, CWID, OPERATIONTIME)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """
            # 准备要插入的数据
            data_to_insert = (
                self.task_identifier,
                self.batch_no,
                self.task_index,
                self.order_no,
                self.production_date,
                self.expiry_date,
                self.images_str,
                self.user_cwid,
                self.operation_time
            )
            # 执行插入操作
            cursor.execute(insert_query, data_to_insert)

            # 提交事务
            connection.commit()

        except Exception as e:
            error=f"插入数据时发生错误: {type(e)}, 错误信息: {e}"

        finally:
            # 无论成功还是失败，都要关闭数据库连接
            cursor.close()
            connection.close()

class LabelThread(QThread):
    def __init__(self, command, working_dir):
        super().__init__()
        self.command = command
        self.working_dir = working_dir

    def run(self):
        self.process = subprocess.Popen(self.command, cwd=self.working_dir)

    def is_running(self):
        # 检查进程是否在运行
        return self.process and self.process.poll() is None

class ImageSaveThread(QThread):
    save_finished = pyqtSignal(str)  # 用于保存完成后发出信号

    def __init__(self, image_np, file_path, file_format='jpg'):
        super().__init__()
        self.image_np = np.asarray(image_np, dtype=np.uint8)  # 确保图像数据类型为uint8
        self.file_path = file_path
        # 转换'jpg'为'JPEG'以确保兼容性
        self.file_format = 'JPEG' if file_format.lower() == 'jpg' else file_format.upper()

    def run(self):
        try:
            img = Image.fromarray(self.image_np).convert('RGB')
            save_path = Path(self.file_path)
            save_path.parent.mkdir(parents=True, exist_ok=True)

            # 保存图像
            img.save(save_path, self.file_format, quality=85)
            self.save_finished.emit(f"图像已保存到 {save_path}")
        except Exception as e:
            self.save_finished.emit(f"保存图像失败: {e}")

class TrainingThread(QThread):
    def __init__(self, divide_dataset_cmd, train_cmd):
        super(TrainingThread, self).__init__()
        self.divide_dataset_cmd = divide_dataset_cmd
        self.train_cmd = train_cmd

    def run(self):
        # 先执行划分数据集的命令
        subprocess.run(self.divide_dataset_cmd, shell=True, check=True)
        # 然后执行训练命令
        subprocess.run(self.train_cmd, shell=True, check=True)