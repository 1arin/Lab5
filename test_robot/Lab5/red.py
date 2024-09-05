import cv2
import numpy as np


lower = np.array([0, 120, 70])
upper = np.array([10, 255, 255])

webcam_video = cv2.VideoCapture(0)

while True:
    success, video = webcam_video.read() 

    img = cv2.cvtColor(video, cv2.COLOR_BGR2HSV) 
    mask = cv2.inRange(img, lower, upper) 

    mask_contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) # Finding contours in mask image

    if len(mask_contours) != 0:
        for mask_contour in mask_contours:
            if cv2.contourArea(mask_contour) > 500:
                x, y, w, h = cv2.boundingRect(mask_contour)
                cv2.rectangle(video, (x, y), (x + w, y + h), (0, 0, 255), 3) #drawing rectangle

    cv2.imshow("mask image", mask) 

    cv2.imshow("window", video) 

    cv2.waitKey(1)