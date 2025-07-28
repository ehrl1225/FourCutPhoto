import time

import numpy as np
from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6.QtGui import QImage

from gui.common import CommonWidget
from image import ImageCapture, ImageEditor, ImageUtil, FourCutData
from util import DataManager


class ImageCaptureWorker(QThread):
    imageCaptured = pyqtSignal(QImage)
    go:bool = True

    def __init__(self, parent:CommonWidget=None):
        super().__init__()
        self.parent = parent
        self.image_util = ImageUtil()
        self.imageCapture = ImageCapture()

    def setCameraID(self, camera_id:int):
        self.imageCapture.setCam(camera_id)

    def setCallback(self, callback):
        self.callback = callback

    def stop(self):
        self.go = False

    def run(self):
        self.imageCapture.openCamera()
        while self.go:
            img = self.imageCapture.capture()
            if img is None:
                continue
            self.callback(img)
            # qt_image = self.image_util.cv2QImage(img)
            # self.imageCaptured.emit(qt_image)
        self.imageCapture.closeCamera()







