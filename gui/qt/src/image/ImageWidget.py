import cv2
from PyQt6.QtGui import QImage, QKeyEvent
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton
from PyQt6.QtCore import pyqtSlot, pyqtSignal

from src.main.printer.Printer import Printer
from src.main.util import DataManager
from .ImageCaptureWidget import ImageCaptureWidget
from .ImageChoosingWidget import ImageChoosingWidget
from .ImagePrintingDoneWidget import ImagePrintingDoneWidget
from .ImagePrintingWidget import ImagePrintingWidget
from .FrameChoosingWidget import FrameChoosingWidget
from enum import Enum

from .ImageShowWidget import ImageShowWidget
from gui.qt.src.common.CommonWidget import CommonWidget


class ImageState(Enum):
    init:int = 0
    take_photo:int = 1


class ImageWidget(CommonWidget):
    done_service = pyqtSignal()

    def __init__(self, parent:CommonWidget=None):
        super().__init__()
        self.current_image:QImage|None = None
        self.data_manager:DataManager = parent.data_manager
        self.initUI()

    def initUI(self):
        self.image_capture_wg = ImageCaptureWidget(self)
        self.frame_choosing_wg = FrameChoosingWidget(self)
        self.image_choosing_wg = ImageChoosingWidget(self)
        self.image_show_wg = ImageShowWidget(self)
        self.image_printing_wg = ImagePrintingWidget(self)
        self.image_printing_done_wg = ImagePrintingDoneWidget(self)


        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.frame_choosing_wg)

        self.current_wg = self.frame_choosing_wg

        self.setLayout(self.vbox)

        self.setUI()

    def setUI(self):

        self.data_manager.loadFourCutDatas()
        self.frame_choosing_wg.setImages()
        self.frame_choosing_wg.go_next.connect(self.toImageCaptureWidget)
        self.image_capture_wg.go_next.connect(self.capturedImages)
        self.image_choosing_wg.go_next.connect(self.toPrintingWidget)
        self.image_show_wg.go_back.connect(self.toImageCaptureWidget)
        self.image_show_wg.go_next.connect(self.toPrintingWidget)
        self.image_printing_wg.go_next.connect(self.toImagePrintingDoneWidget)
        self.image_printing_done_wg.go_next.connect(self.toFrameChoosingWidget)

        # self.data_manager.setSelectedFrameIndex(2)
        # self.toImageCaptureWidget()
        # self.data_manager.setPhotoDirectory("728d9c224257a05ebe09")
        # self.toImageChoosingWidget()
        # for i in range(4):
        #     self.image_choosing_wg.select_image(i)
        # self.image_choosing_wg.setSelectedImages()
        # self.toPrintingWidget()
        # self.toImagePrintingDoneWidget()

    def hideWidget(self, wg:QWidget):
        self.vbox.removeWidget(wg)
        wg.setParent(None)

    def showWidget(self, wg:QWidget):
        self.vbox.addWidget(wg)
        self.current_wg = wg

    def capturedImages(self):
        frame = self.data_manager.getSelectedFrame()
        self.image_capture_wg.endCapture()
        if frame.hasOverlayImages():
            self.toImageShowWidget()
        else:
            self.toImageChoosingWidget()

    def toImageShowWidget(self):
        self.hideWidget(self.current_wg)
        self.image_show_wg.setImages()
        self.showWidget(self.image_show_wg)

    def toImagePrintingDoneWidget(self):
        self.hideWidget(self.current_wg)
        self.showWidget(self.image_printing_done_wg)

    def toImageCaptureWidget(self):
        self.hideWidget(self.current_wg)
        self.startCapture()
        self.showWidget(self.image_capture_wg)

    def toPrintingWidget(self):
        self.hideWidget(self.current_wg)
        self.showWidget(self.image_printing_wg)

    def startCapture(self):
        self.image_capture_wg.startCapture()

    def toFrameChoosingWidget(self):
        self.hideWidget(self.current_wg)
        self.showWidget(self.frame_choosing_wg)
        self.frame_choosing_wg.setImages()
        self.done_service.emit()

    def toImageChoosingWidget(self):
        self.hideWidget(self.current_wg)
        self.image_choosing_wg.setImages()
        self.showWidget(self.image_choosing_wg)

    def keyPressed(self, event:QKeyEvent):
        self.image_capture_wg.onKeyPressEvent(event)

    def keyPressEvent(self, a0):
        self.keyPressed(a0)

    @pyqtSlot(QKeyEvent)
    def onKeyPressEvent(self, event:QKeyEvent):
        self.keyPressed(event)

