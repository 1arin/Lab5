# import cv2
# from robomaster import robot
# import numpy as np
# import matplotlib.pyplot as plt

# # E. Convert the original image to HSL color space. Rescale the L-channel image from to the pixel value range [-1, 1].
# # F. Plot the histogram of rescaled L-channel image.

# image = cv2.imread("test_img.jpg")

# hsl_image = cv2.cvtColor(image, cv2.COLOR_BGR2HLS)

# l_channel = hsl_image[:,:,1]

# l_channel_scaled = (l_channel.astype(float) / 255) * 2 - 1

# plt.hist(l_channel_scaled.ravel(), 256)
# plt.title("Histogram of Rescaled L-channel")
# plt.xlabel("Pixel Value")
# plt.ylabel("Frequency")
# plt.show()

import cv2
import numpy as np
import matplotlib.pyplot as plt

# Load the image
image = cv2.imread("test_img.jpg")

# Convert the original image to HSL color space
hsl_image = cv2.cvtColor(image, cv2.COLOR_BGR2HLS)

# Extract the L-channel
l_channel = hsl_image[:, :, 1]

# Rescale the L-channel image to the pixel value range [-1, 1]
l_channel_scaled = (l_channel.astype(float) / 255) * 2 - 1

# Normalize the scaled L-channel to the range [0, 256] for cv2.calcHist
l_channel_normalized = ((l_channel_scaled + 1) * 128).astype(np.uint8)

# Calculate histogram using cv2.calcHist
hist = cv2.calcHist([l_channel_normalized], [0], None, [256], [0, 256])

# Plot the histogram
plt.plot(hist)
plt.title("Histogram of Rescaled L-channel")
plt.xlabel("Pixel Value")
plt.ylabel("Frequency")
plt.show()
