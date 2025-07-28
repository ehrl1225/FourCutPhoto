

class PrinterTask:
    photo_path:str
    print_count:int

    def __init__(self, photo_path:str, print_count:int):
        self.photo_path = photo_path
        self.print_count = print_count
