import cv2
import numpy as np
import math
from image_helper import copy_with_alpha

nawc_logo = cv2.imread("./Images/LOGO-Kreis.png", -1)
nawc_logo = cv2.resize(nawc_logo, (1000, 1000))


class Canvas():
    def __init__(self):
        self.printable = False
        self.image = None
        self.file = None
        self.border = 8

    def read_image(self, path: str):
        self.image = cv2.imread(filename=path)
        self.file = path
        h, w = self.image.shape[:2]
        if w > h:
            self.image = cv2.rotate(self.image, cv2.ROTATE_90_CLOCKWISE)
            w, h = h, w
        
        if w * math.sqrt(2) > h:
            w = int(h / math.sqrt(2))
            self.image = self.image[:, :w]
        else:
            h = int(w * math.sqrt(2))
            self.image = self.image[:h, :]
        
        h, w = self.image.shape[:2]

        # At this point, h > w, so insert at certain scale at bottom
        size_cm_logo = 2
        nawc_copy = nawc_logo.copy()
        size = int(w * size_cm_logo / 21)
        size = size // 2 * 2
        nawc_copy = cv2.resize(nawc_copy, (size, size))
        self.original_image = self.image.copy()
        self.image[h - nawc_copy.shape[1] - 50:h - 50, w//2 - nawc_copy.shape[0]//2:w // 2 + nawc_copy.shape[0] // 2] = copy_with_alpha(self.image[h - nawc_copy.shape[1] - 50:h - 50, w//2 - nawc_copy.shape[0]//2:w // 2 + nawc_copy.shape[0] // 2], nawc_copy)
        self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        self.image = cv2.cvtColor(self.image, cv2.COLOR_GRAY2BGRA)

    
    def resize_image(self, width: int):
        h, w = self.image.shape[:2]

        ratio = width / w        
        new_size = int(w * ratio), int(h * ratio)
        self.display_image = cv2.resize(self.image, new_size)
        self.output_size = (new_size[1], new_size[0])
        self.canvas_image = np.zeros((self.output_size[0] + 2 * self.border, self.output_size[1] + 2 * self.border, 4), np.uint8)
        if self.printable:
            self.canvas_image[:] = (102, 204, 102, 255)
        else:
            self.canvas_image[:] = (0, 0, 255, 0)

        self.canvas_image[self.border:self.border + self.output_size[0], self.border:self.border + self.output_size[1]] = self.display_image

    def change_printable(self):
        self.printable = not self.printable
        if self.printable:
            self.canvas_image[:] = (102, 204, 102, 255)
        else:
            self.canvas_image[:] = (0, 0, 255, 0)
        self.canvas_image[self.border:self.border + self.output_size[0], self.border:self.border + self.output_size[1]] = self.display_image

    def get_image(self):
        return self.canvas_image

    def get_image_for_printing(self, path):
        cv2.imwrite(path, self.image)

    def get_original_image(self, path):
        cv2.imwrite(path, self.original_image)
    
    def get_image_path(self):
        return self.file