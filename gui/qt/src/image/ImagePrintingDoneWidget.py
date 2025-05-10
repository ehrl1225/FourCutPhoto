from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QLabel, QVBoxLayout, QPushButton

from gui.qt.src.common.CommonWidget import CommonWidget


class ImagePrintingDoneWidget(CommonWidget):
    go_next = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__()
        self.initUI()

    def initUI(self):


        self.background_lb = QLabel(self)

        self.go_next_btn = QPushButton(self)
        self.go_next_btn.setStyleSheet("""
        background-color : black;
        """)

        background_pixmap = QPixmap("./gui/qt/img/printing_done_img.png")

        screen_size = self.screen().size()
        width = screen_size.width()
        height = screen_size.height()
        background_pixmap = background_pixmap.scaled(width, height, Qt.AspectRatioMode.KeepAspectRatio)

        self.background_lb.setPixmap(background_pixmap)

        vbox = QVBoxLayout()
        vbox.addWidget(self.background_lb)

        self.setLayout(vbox)

        self.setUI()

    def setUI(self):
        self.go_next_btn.setGeometry(1100, 400, 350, 100)
        self.go_next_btn.clicked.connect(self.goNext)


    def goNext(self):
        self.go_next.emit()




