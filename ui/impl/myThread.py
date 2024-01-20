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



    def run(self):
        while self._is_running:
            state = mphdc.GetCameraState(self.camera)
            if state == mphdc.DeviceStateType.StandBy:
                res, data = mphdc.SnapCamera(self.camera, 2000)
                if res:
                    imgs, n, channels = mphdc.Nppc_Create(data)
                    if n > 0:
                        # 合并 nx, ny, nz 通道
                        nx_channel = imgs[channels.index(mphdc.ImageContentType.Photometric_Nx),:,:]
                        ny_channel = imgs[channels.index(mphdc.ImageContentType.Photometric_Ny),:,:]
                        nz_channel = imgs[channels.index(mphdc.ImageContentType.Photometric_Nz),:,:]
                        merged_image = cv2.merge([nx_channel, ny_channel, nz_channel])
                        self.image_captured.emit(merged_image)




    def stop(self):
        self._is_running = False

# OCR检测子线程 ocr_instance  self.ocr = ocr_instance  # 使用传入的 PaddleOCR 实例
class OcrThread(QThread):
    finished = pyqtSignal(object)  # 完成信号，传递检测结果

    def __init__(self, images, det_model_dir,rec_model_dir,det_db_unclip_ratio, parent=None):
        super().__init__(parent)
        self.images = images  # NumPy图像数组列表
        self.Ocr=PaddleOCR(det_model_dir=det_model_dir,
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