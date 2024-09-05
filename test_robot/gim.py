import cv2
import robomaster
from robomaster import robot
from robomaster import vision
import time
import matplotlib.pyplot as plt


# A class for storing MarkerInfo
class MarkerInfo:
    # Label center point information (x y axis) Width Length Label information
    def __init__(self, x, y, w, h, info):
        self._x = x
        self._y = y
        self._w = w
        self._h = h
        self._info = info

    # คำนวณมุมซ้ายบนของป้ายและแปลงเป็น pixel
    @property
    def pt1(self):
        return int((self._x - self._w / 2) * 1280), int((self._y - self._h / 2) * 720)

    # คำนวณมุมขวาล่างของป้ายและแปลงเป็น pixel
    @property
    def pt2(self):
        return int((self._x + self._w / 2) * 1280), int((self._y + self._h / 2) * 720)

    # จุดกลางป้ายเป็น pixel
    @property
    def center(self):
        return int(self._x * 1280), int(self._y * 720)

    # Label information
    @property
    def text(self):
        return self._info


markers = []


# in case that there are many detected markers
def on_detect_marker(marker_info):
    number = len(marker_info)
    markers.clear()
    for i in range(0, number):
        x, y, w, h, info = marker_info[i]
        markers.append(
            MarkerInfo(x, y, w, h, info)
        )  # x and y w h is in a range of [0 1] relative to image's size


# เก็บข้อมูลมุมของ gimbal
def sub_data_handler(angle_info):
    global list_of_data
    list_of_data = angle_info


if __name__ == "__main__":
    # initialize robot
    ep_robot = robot.Robot()
    ep_robot.initialize(conn_type="rndis")
    ep_vision = ep_robot.vision
    ep_camera = ep_robot.camera
    ep_gimbal = ep_robot.gimbal
    ep_blaster = ep_robot.blaster
    # the image center constants
    center_x = 1280 / 2
    center_y = 720 / 2
    # frame = 720 / 2

    ep_camera.start_video_stream(display=False)
    ep_gimbal.sub_angle(freq=50, callback=sub_data_handler)
    result = ep_vision.sub_detect_info(name="marker", callback=on_detect_marker)

    # หมุน gimbal กลับไปที่ center
    ep_gimbal.recenter(pitch_speed=200, yaw_speed=200).wait_for_completed()

    count = 0
    time.sleep(1)

    # PID controller constants
    p = -0.607
    i = 0
    d = -0.00135

    # loop การทำงานของหุ่น
    accumulate_err_x = 0
    accumulate_err_y = 0
    data_pitch_yaw = []

    while True:  
        if len(markers) != 0:  # target found
            time = time.time()
            x, y = markers[-1].center  # x,y here in the pixel unit

            err_x = center_x - x  # err_x = image_center in x direction - current marker center in x direction
            err_y = center_y - y  # err_y = image_center in y direction - current marker center in y direction

            accumulate_err_x += err_x
            accumulate_err_y += err_y


            if count >= 1:
                # คำนวณความเร็วในการหมุน gimbal โดยใช้ PID
                speed_x = (p * err_x) + d * ((prev_err_x - err_x) / (prev_time - time)) + i * (accumulate_err_x)
                speed_y = (p * err_y) + d * ((prev_err_y - err_y) / (prev_time - time)) + i * (accumulate_err_y)
                
                ep_gimbal.drive_speed(pitch_speed=speed_y, yaw_speed=-speed_x)

                
                data_pitch_yaw.append(
                    list(list_of_data) + [err_x, err_y, round(speed_x, 3), round(speed_y, 3)]
                # หมุน gimbal ตามความเร็วที่คำนวณมา
                # print(f'this is speed_x : {speed_x}, this is speed_y :{speed_y}')
                )

                # เก็บค่ามุมของ gimbal, error x, error y, speed x, speed y, และ d

            count += 1

            prev_time = time
            prev_err_x = err_x
            prev_err_y = err_y
            time.sleep(0.01)

        else:
            # หมุนกลับ center
            ep_gimbal.drive_speed(pitch_speed=0, yaw_speed=0)

        # อ่านภาพ
        img = ep_camera.read_cv2_image(strategy="newest", timeout=0.5)

        # วาดสี่เหลี่ยมบนภาพในตำแหน่งที่เจอป้าย
        for marker in markers:
            cv2.rectangle(img, marker.pt1, marker.pt2, (0, 255, 0))
            cv2.putText(
                img,
                marker.text,
                marker.center,
                cv2.FONT_HERSHEY_SIMPLEX,
                1.5,
                (0, 255, 0),
                3,
            )
            # cv2.putText(
            #     img,
            #     str(frame%300),
            #     (10,25),
            #     cv2.FONT_HERSHEY_SIMPLEX,
            #     1.5,
            #     (0,255,0),
            #     3,
            # )
        # แสดงภาพ
        cv2.imshow("Markers", img)
        # สำหรับออกจาก loop while
        if cv2.waitKey(1) & 0xFF == ord("x"):
            break

    cv2.destroyAllWindows()

    result = ep_vision.unsub_detect_info(name="marker")
    ep_camera.stop_video_stream()
    ep_robot.close()

    # plot error x, error y, speed x, speed y, and dt
    x_point = range(len(data_pitch_yaw))
    y_point4 = [i[4] for i in data_pitch_yaw]
    y_point5 = [i[5] for i in data_pitch_yaw]
    y_point6 = [i[6] for i in data_pitch_yaw]
    y_point7 = [i[7] for i in data_pitch_yaw]
    
    plt.plot(x_point,y_point4)
    plt.plot(x_point,y_point5)
    plt.plot(x_point,y_point6)
    plt.plot(x_point,y_point7)

    plt.legend(["center_x","x"])
    plt.show()
    

    plt.figure((10,5))
    plt.plot(center_x)