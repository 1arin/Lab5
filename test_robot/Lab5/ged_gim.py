import cv2
import numpy as np

image = cv2.imread('coke_can.jpg')
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

lower_red1 = np.array([0, 100, 100])   # Lower bound for the first red range
upper_red1 = np.array([10, 255, 255])
lower_red2 = np.array([160, 100, 100]) # Lower bound for the second red range
upper_red2 = np.array([180, 255, 255])

mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
mask2 = cv2.inRange(hsv, lower_red2, upper_red2)

mask = cv2.bitwise_or(mask1, mask2)

coke_can_area = cv2.bitwise_and(image, image, mask=mask)

cv2.imshow('Coke Can Mask', mask)
cv2.imshow('Coke Can Area', coke_can_area)
cv2.waitKey(0)
cv2.destroyAllWindows()