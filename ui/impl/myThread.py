import requests
from PyQt5.QtCore import QThread, pyqtSignal, QBuffer, QIODevice
import numpy as np
from mphdcpy import mphdc
import cv2
import paddleocr
from PIL import Image
from io import BytesIO
from paddleocr import PaddleOCR
import ctypes as ct
import time

# 定义图像捕获线程类
class CameraWorker(QThread):
    image_captured = pyqtSignal(np.ndarray)

    def __init__(self, camera):
        super().__init__()
        self.camera = camera
        self._is_running = True
        self._take_photo = False  # 添加一个标志来控制拍照
        print(paddleocr.__version__)

    def run(self):
        while self._is_running:
            state = mphdc.GetCamearState(self.camera)
            if state == mphdc.DeviceStateType.StandBy:
                res, data = mphdc.SanpCamera(self.camera, 2000)
                if res:
                    imgs, n, channels = mphdc.Nppc_Create(data)
                    if n > 0:
                        # 合并 nx, ny, nz 通道
                        nx_channel = imgs[channels.index(mphdc.ImageContentType.Photometric_Nx),:,:]
                        ny_channel = imgs[channels.index(mphdc.ImageContentType.Photometric_Ny),:,:]
                        nz_channel = imgs[channels.index(mphdc.ImageContentType.Photometric_Nz),:,:]
                        merged_image = cv2.merge([nx_channel, ny_channel, nz_channel])
                        self.image_captured.emit(merged_image)

    def take_photo(self):
        self._take_photo = True

    def stop(self):
        self._is_running = False

# OCR检测子线程 ocr_instance  self.ocr = ocr_instance  # 使用传入的 PaddleOCR 实例
class OcrThread(QThread):
    finished = pyqtSignal(object)  # 完成信号，传递检测结果

    def __init__(self, images, det_model_dir, rec_model_dir, parent=None):
        super().__init__(parent)
        self.images = images  # NumPy图像数组列表
        self.det_model_dir = det_model_dir  # 检测模型路径
        self.rec_model_dir = rec_model_dir  # 识别模型路径

    def run(self):
        print("检测模型路径：", self.det_model_dir)
        print("识别模型路径：", self.rec_model_dir)
        # 在此处创建新的 PaddleOCR 实例
        self.ocr = PaddleOCR(det_model_dir=self.det_model_dir,
                             rec_model_dir=self.rec_model_dir,
                             use_angle_cls=True, lang='ch')
        results = []
        for i, image_np in enumerate(self.images):
            # 打印图像信息进行检查
            print(f"Image {i}: shape = {image_np.shape}, dtype = {image_np.dtype}")

            result = self.ocr.ocr(image_np, cls=True)
            results.append((i, result))
        self.finished.emit(results)  # 发送完成信号，附带检测结果