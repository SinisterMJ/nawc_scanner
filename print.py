from PIL import Image, ImageWin
from win32 import win32print
import win32ui


def print_image(image_path):
    """
    Prints an image to the default printer.

    This function opens an image file, scales it to fit the printable area of the default printer, 
    and sends it to the printer for printing.

    Args:
        image_path (str): The file path of the image to be printed.

    Raises:
        OSError: If the image file cannot be opened or processed.
    """    
    # Open the image file
    image = Image.open(image_path)

    # Get the default printer
    printer_name = win32print.GetDefaultPrinter()
    hprinter = win32print.OpenPrinter(printer_name)

    try:
        # Start the print job
        hdc = win32ui.CreateDC()
        hdc.CreatePrinterDC(printer_name)
        printable_area = hdc.GetDeviceCaps(8), hdc.GetDeviceCaps(10)
        printer_size = hdc.GetDeviceCaps(110), hdc.GetDeviceCaps(111)

        # Scale the image to fit the printable area
        ratio = min(printable_area[0] / image.size[0], printable_area[1] / image.size[1])
        scaled_size = int(image.size[0] * ratio), int(image.size[1] * ratio)
        image = image.resize(scaled_size, Image.Resampling.BICUBIC)

        # Convert the image to a format suitable for printing
        hdc.StartDoc("Image Print")
        hdc.StartPage()

        dib = ImageWin.Dib(image)
        dib.draw(hdc.GetHandleOutput(), (0, 0, scaled_size[0], scaled_size[1]))

        hdc.EndPage()
        hdc.EndDoc()
        hdc.DeleteDC()
    finally:
        win32print.ClosePrinter(hprinter)

def get_printable_area():
    # Get the default printer
    printer_name = win32print.GetDefaultPrinter()
    hprinter = win32print.OpenPrinter(printer_name)

    try:
        # Start the print job
        hdc = win32ui.CreateDC()
        hdc.CreatePrinterDC(printer_name)
        printable_area = hdc.GetDeviceCaps(8), hdc.GetDeviceCaps(10)
        hdc.DeleteDC()
    finally:
        win32print.ClosePrinter(hprinter)

    return printable_area