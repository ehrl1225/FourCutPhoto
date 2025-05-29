from PyQt6.QtCore import QThread, pyqtSignal
from src.main.printer import Printer


class PrintWorker(QThread):
    go:bool
    don_printing:pyqtSignal


    def __init__(self, parent=None):
        QThread.__init__(self, parent)
        self.parent = parent
        self.printers:Printer = list()
        self.sub_workers = []
        self.available_workers = []
        self.print_queue = list()
        self.go = True

    def add_print_image(self, print_image):
        self.print_queue.append(print_image)

    def run(self):
        while self.go:
            for worker in self.available_workers:
                worker.set_image_url(self.print_queue.pop(0))
                worker.start()


