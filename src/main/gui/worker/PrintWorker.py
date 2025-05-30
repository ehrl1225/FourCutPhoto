from PyQt6.QtCore import QThread, pyqtSignal

from .PrinterTask import PrinterTask
from src.main.printer import Printer


class PrintWorker(QThread):
    go:bool
    done_printing:pyqtSignal = pyqtSignal()


    def __init__(self, parent=None):
        QThread.__init__(self, parent)
        self.parent = parent
        self.printer = Printer()
        self.task_queue = list()
        self.go = True

    def addTask(self, image_path, print_count):
        printer_task = PrinterTask(image_path, print_count)
        self.task_queue.append(printer_task)

    def run(self):
        while self.go:
            if len(self.task_queue)>0:
                printer_task = self.task_queue.pop(0)
                # self.printer.print_image(printer_task.image_path, printer_task.print_count)
                # self.printer.wait_for_print_completion()
                self.done_printing.emit()
