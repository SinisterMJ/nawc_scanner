import cv2
import numpy as np

# Load the larger image (background)
background = cv2.imread("background.jpg")

# Load the smaller image (foreground) with alpha channel
foreground = cv2.imread("foreground.png", cv2.IMREAD_UNCHANGED)

# Extract the alpha channel from the foreground image
alpha = foreground[:, :, 3] / 255.0  # Normalize alpha to range [0, 1]

# Extract the RGB channels from the foreground image
foreground_rgb = foreground[:, :, :3]

# Define the position where the foreground will be placed on the background
x_offset, y_offset = 50, 100  # Top-left corner of the foreground on the background

# Get the region of interest (ROI) on the background
roi = background[y_offset:y_offset+foreground.shape[0], x_offset:x_offset+foreground.shape[1]]

# Blend the images using the alpha mask
for c in range(3):  # Loop over RGB channels
    roi[:, :, c] = (alpha * foreground_rgb[:, :, c] + (1 - alpha) * roi[:, :, c])

# Replace the ROI on the background with the blended result
background[y_offset:y_offset+foreground.shape[0], x_offset:x_offset+foreground.shape[1]] = roi

# Save or display the result
cv2.imwrite("result.jpg", background)
cv2.imshow("Result", background)
cv2.waitKey(0)
cv2.destroyAllWindows()