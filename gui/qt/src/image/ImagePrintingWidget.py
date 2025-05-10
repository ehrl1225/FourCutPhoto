from unittest import case

from PyQt6.QtCore import pyqtSignal, Qt, QTimer
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout

from gui.qt.src.common.CommonObject import CommonObject
from src.main.image import ImageUtil, ImageEditor

TOTAL_PRINTING_IMAGE_COUNT = 2

class ImagePrintingWidget(QWidget):
    go_next = pyqtSignal()

    def __init__(self, parent:CommonObject=None):
        super().__init__()
        self.parent = parent
        self.data_manager = parent.data_manager
        self.counter = 0
        self.initUI()

    def initUI(self):
        self.background_label = QLabel(self)

        # 테스트용 mac 환경에서는 print 못하는 상황이므로
        self.go_next_btn = QPushButton('go_next', self)
        self.printer_pixmaps = [
            QPixmap("gui/qt/img/printing_img1.png"),
            QPixmap("gui/qt/img/printing_img2.png"),
        ]
        screen_size = self.screen().size()
        width = screen_size.width()
        height = screen_size.height()

        for pixmap_index, pixmap in enumerate(self.printer_pixmaps):
            pixmap = pixmap.scaled(width, height, Qt.AspectRatioMode.KeepAspectRatio)
            self.printer_pixmaps[pixmap_index] = pixmap

        self.background_label.setPixmap(self.printer_pixmaps[0])

        hbox = QHBoxLayout()
        hbox.addStretch()
        hbox.addWidget(self.background_label)
        hbox.addStretch()

        self.go_next_btn.setGeometry(1100, 400, 350, 100)
        self.timer = QTimer()
        self.timer.start(1000)
        self.timer.timeout.connect(self.countDown)


        self.setLayout(hbox)
        self.setUI()

    def setUI(self):
        self.image_util = ImageUtil()
        self.image_editor = ImageEditor()
        self.go_next_btn.pressed.connect(self.returnMain)

    def countDown(self):
        self.background_label.setPixmap(self.printer_pixmaps[self.counter])
        self.counter += 1
        self.counter %= TOTAL_PRINTING_IMAGE_COUNT

    def countDownDone(self):
        self.counter = 0
        self.timer.stop()

    def returnMain(self):
        self.data_manager.clearImages()
        self.countDownDone()
        self.go_next.emit()
