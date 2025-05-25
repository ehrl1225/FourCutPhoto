from PIL import Image, ImageWin
# import win32print
# import win32ui

class Printer:
    def __init__(self):
        # self.printer_name = win32print.GetDefaultPrinter()
        pass

    def set_printer(self, printer_name):
        self.printer_name = printer_name

    def get_printers(self):
        printers = [printer[2] for printer in win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL | win32print.PRINTER_ENUM_CONNECTIONS)]
        printer_names = [printer[2] for printer in printers]
        return printer_names

    def print_image(self, image_path, copies=1):
        """
        Print the image to fit the entire A4 page, with a specified number of copies.
        
        :param image_path: Path to the image file.
        :param copies: Number of copies to print.
        """
        # Open the image file
        image = Image.open(image_path)

        # A4 size in pixels at 300 DPI (standard print resolution)
        a4_width, a4_height = 2480, 3508  # 8.27 x 11.69 inches at 300 DPI

        # Resize the image to fit A4 size while maintaining aspect ratio
        image = image.resize((a4_width, a4_height), Image.ANTIALIAS)

        # Get the printer device context
        hdc = win32ui.CreateDC()
        hdc.CreatePrinterDC(self.printer_name)

        # Start the print job
        hdc.StartDoc(image_path)

        for _ in range(copies):  # Repeat for the specified number of copies
            # Start a new page
            hdc.StartPage()

            # Convert the image to a DIB and draw it
            dib = ImageWin.Dib(image)
            dib.draw(hdc.GetHandleOutput(), (0, 0, a4_width, a4_height))

            # End the current page
            hdc.EndPage()

        # End the print job
        hdc.EndDoc()
        hdc.DeleteDC()

# Example usage
if __name__ == "__main__":
    printer = Printer()
    printer.set_printer("Your Printer Name")
    printer.print_image("path/to/your/image.jpg", copies=1)  # Print 1 copy
