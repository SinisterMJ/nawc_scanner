import cv2
import numpy as np

class Canvas():
    def __init__(self):
        self.printable = False
        self.image = None
        self.file = None

    def read_image(self, path: str):
        self.image = cv2.imread(filename=path)
        self.file = path
    
    def resize_image(self, width: int):
        h, w = self.image.shape[:2]
        ratio = width / w
        
        new_size = int(w * ratio), int(h * ratio)
        self.image = cv2.resize(self.image, new_size)
        self.output_size = (new_size[1], new_size[0])

    def get_image(self):
        canvas_image = np.zeros((self.output_size[0] + 30, self.output_size[1] + 30, 3), np.uint8)
        if self.printable:
            canvas_image[:] = (0, 255, 0)
        else:
            canvas_image[:] = (0, 0, 255)

        canvas_image[15:15 + self.output_size[0], 15:15 + self.output_size[1]] = self.image
        return canvas_image
