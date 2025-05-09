import cv2
import numpy as np


def copy_with_alpha(destination, x_offset, y_offset, source):
    """
    Copies a source image with an alpha channel onto a destination image at the specified offset.
    
    :param destination: The destination image (background).
    :param x_offset: The x-coordinate offset for placing the source image.
    :param y_offset: The y-coordinate offset for placing the source image.
    :param source: The source image (foreground) with an alpha channel.
    """
    # Extract the alpha channel from the source image
    alpha = source[:, :, 3] / 255.0  # Normalize alpha to range [0, 1]

    # Extract the RGB channels from the source image
    source_rgb = source[:, :, :3]

    # Get the region of interest (ROI) on the destination image
    roi = destination[y_offset:y_offset + source.shape[0], x_offset:x_offset + source.shape[1]]

    # Blend the images using the alpha mask
    for c in range(3):  # Loop over RGB channels
        roi[:, :, c] = (alpha * source_rgb[:, :, c] + (1 - alpha) * roi[:, :, c])

    # Replace the ROI on the destination with the blended result
    destination[y_offset:y_offset + source.shape[0], x_offset:x_offset + source.shape[1]] = roi
    return destination