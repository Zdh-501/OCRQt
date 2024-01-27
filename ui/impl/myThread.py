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

    def __init__(self, images, det_model_dir,rec_model_dir,det_db_unclip_ratio, parent=None):
        super().__init__(parent)
        self.images = images  # NumPy图像数组列表
        self.Ocr=PaddleOCR(use_gpu=False,
                           det_model_dir=det_model_dir,
                             rec_model_dir=rec_model_dir,
                             use_angle_cls=True,
                             det_db_thresh=0.5,
                             det_db_unclip_ratio=det_db_unclip_ratio,
                             lang='ch')
        print('Ocr',paddleocr.__version__)

    def run(self):
        results = []
        for i, image_np in enumerate(self.images):
            # 打印原始图像大小
            print(f"Original image {i} size: {image_np.shape}")

            # 调整图像大小
            # 假设我们想要将图像的最长边限制为960像素
            scale_factor = 960 / max(image_np.shape[:2])
            width = int(image_np.shape[1] * scale_factor)
            height = int(image_np.shape[0] * scale_factor)
            dim = (width, height)
            resized_image = cv2.resize(image_np, dim, interpolation=cv2.INTER_AREA)

            # 打印调整后的图像大小
            print(f"Resized image {i} size: {resized_image.shape}")


            result = self.Ocr.ocr(resized_image, cls=True)
            results.append((i, result))


        self.finished.emit(results)  # 发送完成信号，附带检测结果

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

    def __init__(self, image, file_path, file_format):
        super().__init__()
        self.image = image
        self.file_path = file_path
        self.file_format = file_format

    def run(self):
        # 使用pathlib处理路径
        save_path = Path(self.file_path)

        # 确保目录存在
        save_path.parent.mkdir(parents=True, exist_ok=True)

        # 定义缩放比例（例如，缩小到原来的50%）
        scale_percent = 50
        width = int(self.image.shape[1] * scale_percent / 100)
        height = int(self.image.shape[0] * scale_percent / 100)
        dim = (width, height)

        # 缩放图像
        resized_image = cv2.resize(self.image, dim, interpolation=cv2.INTER_AREA)

        # 将图像编码为指定的格式
        ext = f'.{self.file_format.lower()}'
        result, encoded_image = cv2.imencode(ext, resized_image)
        if result:
            # 将编码后的图像写入文件
            try:
                with open(save_path, 'wb') as file:
                    file.write(encoded_image)
                self.save_finished.emit(f"图像已保存到 {save_path}")
            except Exception as e:
                self.save_finished.emit(f"保存图像失败: {e}")
        else:
            self.save_finished.emit("图像编码失败")