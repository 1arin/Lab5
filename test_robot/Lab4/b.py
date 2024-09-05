import cv2
from robomaster import robot
import numpy as np
import matplotlib.pyplot as plt

# B. Show the original image from A. and print the size of the image.

image = cv2.imread("test_img.jpg")

if image is not None:
    # ได้รับขนาดของภาพ
    height, width, channels = image.shape
    print(f"Width: {width}, Height: {height}, Channels: {channels}")

    cv2.imshow('Image', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

else:
    print("Failed to load image")