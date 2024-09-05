import cv2
from robomaster import robot
import numpy as np
import matplotlib.pyplot as plt

# G. Create a random noise image with equal size of original image. Random with normal distribution (zero mean, unit variance). Show the noise image.
# H. Combine the noise image with rescaled L-channel image. Show the results image.
# I. Rescale L-channel image back to original pixel value [0, 255]. Convert back to RGB color-space image. Show the result image.
image = cv2.imread("test_img.jpg")
hsl_image = cv2.cvtColor(image, cv2.COLOR_BGR2HLS)
l_channel = hsl_image[:,:,1]
l_channel_scaled = (l_channel.astype(float) / 255) * 2 - 1

noise = np.random.normal(0, 1, l_channel.shape)

cv2.imshow('Random Noise', noise)
cv2.waitKey()
cv2.destroyAllWindows() 

combined_image = l_channel_scaled + noise

cv2.imshow('Combine image', combined_image)
cv2.waitKey()
cv2.destroyAllWindows() 

l_channel_back = ((combined_image + 1) / 2 * 255).astype(np.uint8)
h_channel = hsl_image[:,:,0]
s_channel = hsl_image[:,:,2]

hsv_image = cv2.merge([h_channel, s_channel, l_channel_back])



rgb_image = cv2.cvtColor(hsv_image, cv2.COLOR_HSV2BGR)

plt.imshow(cv2.cvtColor(rgb_image, cv2.COLOR_BGR2RGB))
plt.title("Reconstructed RGB Image")
plt.axis('off')
plt.show()