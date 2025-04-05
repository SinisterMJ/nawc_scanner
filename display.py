import cv2
import numpy as np
from screeninfo import get_monitors
from scanned_page import Canvas

res_x = get_monitors()[0].width
res_y = get_monitors()[0].height
scale = 0.35

printer = cv2.imread("nawc/scanner/Printer.jpg")
finish = cv2.imread("nawc/scanner/495473.png")
finish = cv2.resize(finish, (printer.shape[0], printer.shape[1]))

_FULL_FRAMES = {}

def show_fullscreen(image, background_colour = None, window_name='window', display_number = 0, display_sizes=None):
    """
    Draw a fullscreen image.

    :param image: The image to show.
        If integer, it will be assumed to be in range [0..255]
        If float, it will be assumed to be in range [0, 1]
    :param background_colour: The background colour, as a BGR tuple.
    :param window_name: Name of the window (can be used to draw multiple fullscreen windows)
    :param display_number: Which monitor to display to.
    :param display_sizes: Size of displays (needed only if adding a background colour)
    """
    if image.dtype=='float':
        image = (image*255.999).astype(np.uint8)
    else:
        image = image.astype(np.uint8, copy=False)
    if image.ndim==2:
        image = image[:, :, None]

    assert display_number in (0, 1), 'Only 2 displays supported for now.'
    if window_name not in _FULL_FRAMES:
        cv2.namedWindow(window_name, cv2.WND_PROP_FULLSCREEN)
        if display_number == 1:
            assert display_sizes is not None
            first_display_size = display_sizes[0]
            cv2.moveWindow(window_name, *first_display_size)
        cv2.setWindowProperty(window_name,cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
        if background_colour is not None:
            background_colour = np.array(background_colour)
            if background_colour.dtype=='int':
                background_colour = background_colour.astype(np.uint8)
            else:
                background_colour = (background_colour*255.999).astype(np.uint8)
            assert display_sizes is not None, "Unfortunately, if you want to specify background color you need to specify display sizes."
            pic_display_size = display_sizes[display_number]
            aspect_ratio = pic_display_size[1]/float(pic_display_size[0])  # (hori/vert)
            frame_size_x = int(max(image.shape[0]/aspect_ratio, image.shape[1]))
            frame_size_y = int(max(image.shape[1]*aspect_ratio, image.shape[0]))
            _FULL_FRAMES[window_name] = np.zeros((frame_size_y, frame_size_x, 3), dtype=np.uint8) + background_colour
        else:
            _FULL_FRAMES[window_name] = None

    if _FULL_FRAMES[window_name] is not None:
        frame = _FULL_FRAMES[window_name]
        start_y, start_x = (frame.shape[0] - image.shape[0])//2, (frame.shape[1] - image.shape[1])//2
        frame[start_y: start_y+image.shape[0], start_x:start_x+image.shape[1]] = image
        display_img = frame
    else:
        display_img = image

    cv2.imshow(window_name, display_img)
    cv2.waitKey(1)

def get_all(image_list, offset: int = 0):
    if len(image_list) == 0:
        image = cv2.imread(filename="nawc/scanner/black_background_red_color_paint_explosion_burst_9844_1920x1080.jpg")
        image = cv2.resize(image, (res_x, res_y))
        return image, True
    else:
        curr_offset = 30

        image = cv2.imread(filename="nawc/scanner/PCGGiJM-dota-2-wallpapers.jpg")
        image = cv2.resize(image, (res_x, res_y))

        size_left = 0
        size_right = 0

        image[res_y - 800: res_y - 800 + printer.shape[0], res_x - 300: res_x - 300 + printer.shape[1]] = printer
        image[res_y - 300: res_y - 300 + finish.shape[0], res_x - 300: res_x - 300 + finish.shape[1]] = finish
        
        for idx, canvas in enumerate(image_list):
            x_offset = 0
            if idx % 2 == 1:
                x_offset = int(res_x * scale + 60)

            canvas.resize_image(width = int(res_x * scale))
            image_scan = canvas.get_image()
            x_res = image_scan.shape[1]
            y_res = image_scan.shape[0]
            
            if idx % 2 == 0:
                size_left = y_res
            else:
                size_right = y_res

            target_y_top = max(0, curr_offset - offset)
            target_y_bottom = min(image.shape[0], curr_offset - offset + y_res)

            image_y_top = max(0, offset - curr_offset)
            image_y_bottom = min(image.shape[0] - curr_offset + offset + image_y_top, y_res)

            y_res = image_y_bottom - image_y_top

            if y_res > 0:
                image[target_y_top:target_y_bottom, 30 + x_offset:30 + x_offset + x_res] = image_scan[image_y_top:image_y_bottom, 0:x_res]

            if idx % 2 == 1:
                curr_offset += max(size_left, size_right) + 30

        if len(image_list) % 2 == 1:
            curr_offset += size_left + 30

        if (curr_offset - offset) > image.shape[0]:
            return image, False

        return image, True
    

def get_index_clicked(x: int, y: int, offset: int, image_list: list = None):
    if len(image_list) == 0:
        return -1
    
    curr_offset = 30
    size_left = 0
    size_right = 0
    for idx, canvas in enumerate(image_list):
        x_offset = 0
        if idx % 2 == 1:
            x_offset = int(res_x * scale + 60)

        canvas.resize_image(width = int(res_x * scale))
        image_scan = canvas.get_image()
        x_res = image_scan.shape[1]
        y_res = image_scan.shape[0]
        
        if idx % 2 == 0:
            size_left = y_res
        else:
            size_right = y_res
        
        target_y_top = max(0, curr_offset - offset)
        target_y_bottom = min(res_y, curr_offset - offset + y_res)

        if target_y_top <= y <= target_y_bottom and x_offset <= x <= x_offset + x_res:
            return idx

        if idx % 2 == 1:
            curr_offset += max(size_left, size_right) + 30


def print_clicked(x: int, y:int) -> bool:
    return (res_y - 800) <= y <= (res_y - 800 + printer.shape[0]) and (res_x - 300) <= x <= (res_x - 300 + printer.shape[1])

def finish_clicked(x: int, y:int) -> bool:
    return (res_y - 300) <= y <= (res_y - 300 + printer.shape[0]) and (res_x - 300) <= x <= (res_x - 300 + printer.shape[1])

        