import cv2
from robomaster import robot
import numpy as np
import matplotlib.pyplot as plt

################### B ################

image = cv2.imread("test_img.jpg")

if image is not None:
    # ได้รับขนาดของภาพ
    height, width, channels = image.shape
    print(f"Width: {width}, Height: {height}, Channels: {channels}")

    # cv2.imshow('Image', image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

else:
    print("Failed to load image")

################### B ####################
# แปลง RGB เป็น HSL
hsl_image = cv2.cvtColor(image, cv2.COLOR_BGR2HLS)
# แยกช่อง L
l_channel = hsl_image[:,:,1]
# แสดงภาพช่อง L
plt.imshow(l_channel, cmap='gray')
plt.title("L-channel Image")
plt.axis('off')
plt.show()
################### C ####################
################### D ####################
plt.hist(l_channel.ravel(), 256, [0,256])
plt.title("Histogram of L-channel")
plt.xlabel("Pixel Value")
plt.ylabel("Frequency")
plt.show()
################### D ####################
################### E ####################
l_channel_scaled = (l_channel.astype(float) / 255) * 2 - 1
################### E ####################
################### F ####################
plt.hist(l_channel_scaled.ravel(), 256)
plt.title("Histogram of Rescaled L-channel")
plt.xlabel("Pixel Value")
plt.ylabel("Frequency")
plt.show()
################### F ####################
################### G ####################
noise = np.random.normal(0, 1, l_channel.shape)

plt.imshow(noise, cmap='gray')
plt.title("Random Noise Image")
plt.axis('off')
plt.show()
################### G ####################
################### H ####################
combined_image = l_channel_scaled + noise

plt.imshow(combined_image, cmap='gray')
plt.title("Combined Image (L-channel + Noise)")
plt.axis('off')
plt.show()
################### H ####################
################### I ####################
l_channel_back = ((combined_image + 1) / 2 * 255).astype(np.uint8)
hsl_image[:,:,1] = l_channel_back
rgb_image = cv2.cvtColor(hsl_image, cv2.COLOR_HLS2BGR)

plt.imshow(cv2.cvtColor(rgb_image, cv2.COLOR_BGR2RGB))
plt.title("Reconstructed RGB Image")
plt.axis('off')
plt.show()
################### I ####################
################### J ####################
kernel_size = 6
l_channel_blurred = cv2.boxFilter(l_channel_back, -1, (kernel_size, kernel_size))
hsl_image[:,:,1] = l_channel_blurred
rgb_image_blurred = cv2.cvtColor(hsl_image, cv2.COLOR_HLS2BGR)

plt.imshow(cv2.cvtColor(rgb_image_blurred, cv2.COLOR_BGR2RGB))
plt.title("Blurred and Reconstructed RGB Image")
plt.axis('off')
plt.show()
################### J ####################



# hsl_image = cv2.cvtColor(image, cv2.COLOR_BGR2HLS)
# l_channel = hsl_image[:,:,1]
# l_channel_scaled = (l_channel.astype(float) / 255) * 2 - 1

# noise = np.random.normal(0, 1, l_channel.shape)
# combined_image = l_channel_scaled 
# l_channel_back = ((combined_image + 1) / 2 * 255).astype(np.uint8)
# hsl_image[:,:,1] = l_channel_back
# rgb_image = cv2.cvtColor(hsl_image, cv2.COLOR_HLS2BGR)

# kernel_size = 6
# l_channel_blurred = cv2.boxFilter(l_channel_back, -1, (kernel_size, kernel_size))
# hsl_image[:,:,1] = l_channel_blurred
# rgb_image_blurred = cv2.cvtColor(hsl_image, cv2.COLOR_HLS2BGR)

# plt.imshow(cv2.cvtColor(rgb_image_blurred, cv2.COLOR_BGR2RGB))
# plt.title("Blurred and Reconstructed RGB Image")
# plt.axis('off')
# plt.show()

# if noise is not None:
#     # ได้รับขนาดของภาพ
#     height, width, channels = noise.shape
#     print(f"Width: {width}, Height: {height}, Channels: {channels}")

##3
# plt.imshow(l_channel, cmap='gray')
# plt.title("L-channel Image")
# plt.axis('off')
# plt.show()

# plt.hist(l_channel.ravel(), 256, [0,256])
# plt.title("Histogram of L-channel")
# plt.xlabel("Pixel Value")
# plt.ylabel("Frequency")
# plt.show()

# plt.hist(l_channel_scaled.ravel(), 256)
# plt.title("Histogram of Rescaled L-channel")
# plt.xlabel("Pixel Value")
# plt.ylabel("Frequency")
# plt.show()

# plt.imshow(noise, cmap='gray')
# plt.title("Random Noise Image")
# plt.axis('off')
# plt.show()

# plt.imshow(combined_image, cmap='gray')
# plt.title("Combined Image (L-channel + Noise)")
# plt.axis('off')
# plt.show()

# plt.imshow(cv2.cvtColor(rgb_image, cv2.COLOR_BGR2RGB))
# plt.title("Reconstructed RGB Image")
# plt.axis('off')
# plt.show()