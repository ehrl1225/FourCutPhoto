from PIL import Image, ImageWin

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

    def print_image(self, image_path):
        # Open the image file
        image = Image.open(image_path)

        # A4 size in pixels at 300 DPI (standard print resolution)
        a4_width, a4_height = 2480, 3508  # 8.27 x 11.69 inches at 300 DPI

        # Resize the image to fit A4 width while maintaining aspect ratio
        image = image.resize((a4_width, int(image.height * (a4_width / image.width))), Image.ANTIALIAS)

        # Calculate the height of each split (divide into 4 parts)
        split_height = image.height // 4

        # Get the printer device context
        hdc = win32ui.CreateDC()
        hdc.CreatePrinterDC(self.printer_name)

        # Start the print job
        hdc.StartDoc(image_path)

        for i in range(4):
            # Crop the image to the current section
            cropped_image = image.crop((0, i * split_height, a4_width, (i + 1) * split_height))

            # Start a new page for each section
            hdc.StartPage()

            # Convert the cropped image to a DIB and draw it
            dib = ImageWin.Dib(cropped_image)
            dib.draw(hdc.GetHandleOutput(), (0, 0, a4_width, split_height))

            # End the current page
            hdc.EndPage()

        # End the print job
        hdc.EndDoc()
        hdc.DeleteDC()

# Example usage
if __name__ == "__main__":
    printer = Printer()
    printer.set_printer("Your Printer Name")
    printer.print_image("path/to/your/image.jpg")
