import cv2
import numpy as np
import time
from device_change import create_listener
import glob
from display import get_all, show_fullscreen, get_index_clicked
from display import print_clicked, finish_clicked
from scanned_page import Canvas
from print import print_image
import win32gui
import win32con

image_list = []
fps = 1
offset = 0
max_scroll = False

def callback_arrival(letter: str):
    """
    Handles the event when a new device is connected.

    This function scans the connected device for image files in the DCIM directory, 
    loads them into `Canvas` objects, and appends them to the global `image_list`. 
    It also resets the scrolling offset, maximum scroll flag, and updates the frame rate.

    Args:
        letter (str): The drive letter of the connected device.
    """
    file_list = glob.glob(letter + ":\\DCIM\\*\\*.jpg")
    for file in file_list:
        canvas = Canvas()
        canvas.read_image(file)
        image_list.append(canvas)
    global fps
    global offset
    global max_scroll
    offset = 0
    max_scroll = False
    fps = 30


def callback_removal():
    """
    Handles the event when a device is disconnected.

    This function clears the global `image_list` and resets the frame rate to its default value.
    """
    image_list.clear()
    global fps
    fps = 1


t = create_listener(callback_arrival, callback_removal)


def display_image():
    global max_scroll
    res, max_scroll = get_all(image_list, offset=offset)
    show_fullscreen(res, background_colour=(128, 255, 0), display_sizes=[(1920, 1080), (2560, 1600)], display_number=0, window_name="NAWC Scanner")


def print_selected():
    for canvas in image_list:
        if canvas.printable:
            print_image(canvas.file)
            canvas.printable = False
            time.sleep(0.5)


def finish_device():
    for canvas in image_list:
        pass
        # Delete files here


def click_event(event, x, y, flags, param):    
    global offset
    global max_scroll
    if event == cv2.EVENT_MOUSEWHEEL:
        offset += 50 if flags < 0 else -50
        if max_scroll:
            offset -= 50

        if offset < 0:
            offset = 0
    if event == cv2.EVENT_LBUTTONDOWN:
        global image_list

        if print_clicked(x, y):
            print_selected()
            return
        
        if finish_clicked(x, y):
            finish_device()
            return
        
        index = get_index_clicked(x, y, offset, image_list)
        if index != -1:
            image_list[index].change_printable()

# Initialize window
display_image()
cv2.setMouseCallback("NAWC Scanner", click_event)

index = 0
while True:
    start = time.time()
    display_image()
    end = time.time()
    wait_time = int((1 / fps - (end - start)) * 1000)
    if wait_time > 0:
        k = cv2.waitKey(wait_time) & 0xFF
    else:
        k = cv2.waitKey(1) & 0xFF

    if k == 27:
        break

handle_window = win32gui.FindWindow(None, "Device Change Demo")
win32gui.SendMessage(handle_window, win32con.WM_QUIT, 0, 0)
t.join()
