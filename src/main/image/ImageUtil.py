import cv2
import numpy as np
from PyQt6.QtGui import QImage, QPixmap


class ImageUtil:

    def __init__(self):
        pass

    def cv2QImage(self, img) -> QImage:
        rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        h,w,ch = img.shape
        bytesPerLine = ch * w
        qt_image = QImage(rgb_img.data, w, h, bytesPerLine, QImage.Format.Format_RGB888)
        return qt_image

    def cv2QPixmap(self, img):
        qt_image = self.cv2QImage(img)
        return QPixmap(qt_image)

    def QImage2ndarray(self, qImage:QImage) -> np.ndarray:
        qImage = qImage.convertToFormat(QImage.Format.Format_RGB888)

        width, height = qImage.width(), qImage.height()
        ptr = qImage.bits()
        ptr.setsize(qImage.byteCount())

        arr = np.array(ptr, dtype=np.uint8).reshape(height, width, 3)
        return arr

    def saveImage(self, file_name:str, img:np.ndarray):
        cv2.imwrite(file_name, img)