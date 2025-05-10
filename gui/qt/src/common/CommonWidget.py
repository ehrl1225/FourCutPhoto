from PyQt6.QtWidgets import QWidget

from .CommonObject import CommonObject


class CommonWidget(QWidget, CommonObject):
    def __init__(self, parent:CommonObject=None):
        super().__init__(parent)