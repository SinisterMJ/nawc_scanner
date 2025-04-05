from PIL import Image, ImageWin
from win32 import win32print
import win32ui

# def click_event(event, x, y, flags, param):
#     if event == cv2.EVENT_LBUTTONDOWN:
#         blue = img[x, y, 0]
#         green = img[x, y, 1]
#         red = img[x, y, 2]
#         print(blue, ' ', green, ' ', red)
#         print(x, ' ', y)
#     if event == cv2.EVENT_MOUSEWHEEL:
#         print(flags > 0)


# img = np.zeros((577, 433, 3), np.uint8)

# print(img.shape)
# cv2.imshow('image', img)
# cv2.setMouseCallback('image', click_event)

# cv2.waitKey(0)
# cv2.destroyAllWindows()

def print_image(image_path):
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

# Example usage
# image_path = "C:\\Users\\Anton Roth\\Pictures\\58c316fe5f3ca81d008b4851.jpg"
# print_image(image_path)