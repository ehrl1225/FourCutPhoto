import time

import numpy as np
from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6.QtGui import QImage
from src.main.image import ImageCapture, ImageEditor
from src.main.image.ImageUtil import ImageUtil


class ImageCaptureWorker(QThread):
    imageCaptured = pyqtSignal(QImage)
    go:bool = True
    save_image:bool = False
    save_image_path:str = ""
    save_video:bool = False
    start_time = time.time()
    count_second:int = 0

    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.data_manager = parent.data_manager

    def saveImage(self, save_image_path:str):
        self.save_image_path = save_image_path
        self.save_image = True

    def saveVideo(self, save_video_path:str, seconds:int):
        self.save_video_path = save_video_path
        self.save_video = True
        self.start_time = time.time()
        self.count_second = seconds

    def __saveImage(self, imageCapture:ImageCapture, img:np.ndarray):
        imageCapture.save_image(self.save_image_path, img)
        self.data_manager.images.append(img)
        self.save_image = False
        self.save_image_path = ""

    def __saveVideo(self, imageCapture:ImageCapture, img:np.ndarray):
        current_time = time.time()
        current_seconds = current_time - self.start_time
        if current_seconds > self.count_second:
            self.save_video = False
            self.save_video_path = ""
            return

    def stop(self):
        self.go = False

    def run(self):
        imageCapture = ImageCapture()
        imageCapture.openCamera()
        image_util = ImageUtil()
        image_editor = ImageEditor()
        while self.go:
            img = imageCapture.capture()
            if img is None:
                continue
            qt_image = image_util.cv2QImage(img)
            self.imageCaptured.emit(qt_image)
            if self.save_image:
                self.__saveImage(imageCapture, img)
        imageCapture.closeCamera()







