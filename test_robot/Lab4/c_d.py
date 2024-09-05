import cv2
from robomaster import robot
import numpy as np
import matplotlib.pyplot as plt

# C. Convert the original RGB image to HSL color space image. Show the L-channel image.
# D. Convert the original RGB image to HSL color space image. Plot the histogram of L-channel image.

image = cv2.imread("test_img.jpg")

hsl_image = cv2.cvtColor(image, cv2.COLOR_BGR2HLS)

l_channel = hsl_image[:,:,1]


cv2.imshow('L-Channel', l_channel)
cv2.waitKey()
cv2.destroyAllWindows() 

hist = cv2.calcHist([l_channel], [0], None, [256], [0, 256])
plt.plot(hist)
plt.title("Histogram of L-channel")
plt.xlabel("Pixel Value")
plt.ylabel("Frequency")
plt.show()