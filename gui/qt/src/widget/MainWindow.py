from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QKeyEvent
from PyQt6.QtWidgets import QMainWindow

from gui.qt.src.common.CommonObject import CommonObject
from gui.qt.src.widget.MainWidget import MainWidget
from gui.qt.src.widget.SettingWidget import SettingWidget
from src.main.util import DataManager

TEST_MODE = False

class MainWindow(QMainWindow, CommonObject):
    key_pressed = pyqtSignal(QKeyEvent)

    def __init__(self):
        super().__init__()
        self.data_manager = DataManager()
        self.initUI()

    def initUI(self):
        self.wg = MainWidget(self)
        self.setting_wg = SettingWidget(self)
        self.setCentralWidget(self.wg)
        self.showFullScreen()

        self.setUI()

    def setUI(self):
        if TEST_MODE:
            self.setting_wg.show()

    def setSettings(self):
        self.setting_wg.show()

    def keyPressEvent(self, a0):
        self.wg.onKeyPressEvent(a0)
        self.key_pressed.emit(a0)



