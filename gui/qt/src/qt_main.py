from PyQt6.QtWidgets import QApplication
import sys

from gui.qt.src.widget.MainWindow import MainWindow


def qt_main():
    app = QApplication(sys.argv)
    wg = MainWindow()
    wg.show()
    sys.exit(app.exec())

