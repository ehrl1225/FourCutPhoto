from PIL import Image, ImageWin
import win32print
import win32ui
import time

class Printer:
    def __init__(self):
        self.printer_name = win32print.GetDefaultPrinter()

    def set_printer(self, printer_name):
        self.printer_name = printer_name

    def get_printers(self):
        printers = [printer for printer in win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL | win32print.PRINTER_ENUM_CONNECTIONS)]
        printer_names = [printer[2] for printer in printers]
        return printer_names

    def print_image(self, image_path, copies=1):
        """
        Print the image to fit a 4x6 inch page, with a specified number of copies.
        
        :param image_path: Path to the image file.
        :param copies: Number of copies to print.
        """
        # Open the image file
        image = Image.open(image_path)

        # 4x6 inch size in pixels at 300 DPI (standard print resolution)
        width_4x6, height_4x6 = 1200, 1800  # 4 x 6 inches at 300 DPI

        # Resize the image to fit 4x6 size while maintaining aspect ratio
        image = image.resize((width_4x6, height_4x6), Image.Resampling.LANCZOS)

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
            dib.draw(hdc.GetHandleOutput(), (0, 0, width_4x6, height_4x6))

            # End the current page
            hdc.EndPage()

        # End the print job
        hdc.EndDoc()
        hdc.DeleteDC()

    def wait_for_print_completion(self):
        """
        Wait for the print job to complete.
        """
        printer_handle = win32print.OpenPrinter(self.printer_name)
        try:
            while True:
                # Get the printer status
                printer_status = win32print.GetPrinter(printer_handle, 2)
                jobs = printer_status.get("Jobs", 0)

                # If there are no jobs left, the print is complete
                if jobs == 0:
                    break

                # Wait for a short interval before checking again
                time.sleep(1)
        finally:
            win32print.ClosePrinter(printer_handle)

# Example usage
if __name__ == "__main__":
    printer = Printer()
    printer.set_printer("Your Printer Name")
    printer.print_image("path/to/your/image.jpg", copies=1)  # Print 1 copy
