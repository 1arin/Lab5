import cv2
import numpy as np
import matplotlib.pyplot as plt

def detect_coke_can(image_path):
    # อ่านรูปภาพ
    image = cv2.imread(image_path)
    
    # a. แปลง RGB เป็น HSV
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    # b. กำหนดขอบเขตสีแดงของกระป๋องโค้ก
    lower_red1 = np.array([0, 100, 100])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([160, 100, 100])
    upper_red2 = np.array([180, 255, 255])
    
    # สร้าง mask สำหรับสีแดง
    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
    mask = mask1 + mask2
    
    # ทำ morphological operations เพื่อลดสัญญาณรบกวน
    kernel = np.ones((5,5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    
    # หา contours
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # หา contour ที่ใหญ่ที่สุด (น่าจะเป็นกระป๋องโค้ก)
    if contours:
        largest_contour = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(largest_contour)
        
        # วาดกรอบรอบกระป๋องโค้ก
        cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
    
    # แสดงผลลัพธ์
    plt.figure(figsize=(12, 4))
    plt.subplot(131)
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.title('Detected Coke Can')
    plt.subplot(132)
    plt.imshow(mask, cmap='gray')
    plt.title('Mask')
    plt.subplot(133)
    plt.imshow(hsv[:,:,0], cmap='hsv')
    plt.title('Hue Channel')
    plt.show()
    
    return image, mask

# ทดสอบฟังก์ชัน
image_path = 'path/to/your/coke_can.jpg'  # แทนที่ด้วย path ของรูปภาพจริง
result_image, mask = detect_coke_can(image_path)