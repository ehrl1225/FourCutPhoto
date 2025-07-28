from PyQt6.QtCore import pyqtSlot, pyqtSignal
from PyQt6.QtGui import QKeyEvent
from PyQt6.QtWidgets import QVBoxLayout

from gui.image import ImageWidget
from .SelectPeopleNumberWidget import SelectPeopleNumberWidget
from .WelcomeWidget import WelcomeWidget
from gui.common import CommonWidget


class MainWidget(CommonWidget):
    key_pressed = pyqtSignal(QKeyEvent)

    def __init__(self, parent=None):
        super().__init__()
        self.data_manager = parent.data_manager
        self.initUI()

    def initUI(self):
        self.welcome_wg = WelcomeWidget(self)
        self.spn_wg = SelectPeopleNumberWidget(self)
        self.img_wg = ImageWidget(self)

        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.welcome_wg)

        self.setLayout(self.vbox)

        self.setUI()

        # Set background image
        # self.set_background_image("path/to/your/background.jpg")
        # self.goSelectPeopleNumber()
        # self.goImage()
        # self.finishService()
        # self.goSelectPeopleNumber()

    def setUI(self):
        self.welcome_wg.go_next.connect(self.goSelectPeopleNumber)
        self.spn_wg.go_next.connect(self.goImage)
        self.img_wg.done_service.connect(self.finishService)

    def goSelectPeopleNumber(self):
        self.vbox.removeWidget(self.welcome_wg)
        self.welcome_wg.setParent(None)
        self.vbox.addWidget(self.spn_wg)

    def goImage(self):
        self.vbox.removeWidget(self.spn_wg)
        self.spn_wg.setParent(None)
        self.vbox.addWidget(self.img_wg)

    def finishService(self):
        self.vbox.removeWidget(self.img_wg)
        self.img_wg.setParent(None)
        self.vbox.addWidget(self.welcome_wg)


    @pyqtSlot(QKeyEvent)
    def onKeyPressEvent(self, event: QKeyEvent):
        self.img_wg.onKeyPressEvent(event)
        self.key_pressed.emit(event)
