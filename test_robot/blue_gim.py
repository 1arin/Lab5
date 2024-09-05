import cv2
import robomaster
from robomaster import robot
from robomaster import vision
from robomaster import blaster
import time
import math
import pandas as pd
import matplotlib.pyplot as plt




# คลาสสำหรับเก็บข้อมูล marker(ป้าย)
class MarkerInfo:
    # ข้อมูลจุดตรงกลางป้าย ความกว้าง ความยาว ข้อมูลป้าย
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


    # ข้อมูลป้าย
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


    ep_camera.start_video_stream(display=False)
    ep_gimbal.sub_angle(freq=10, callback=sub_data_handler)
    result = ep_vision.sub_detect_info(name="marker", callback=on_detect_marker)


    # หมุน gimbal กลับไปที่ center
    ep_gimbal.recenter(pitch_speed=200, yaw_speed=200).wait_for_completed()


    count = 0
    time.sleep(1)


    # PID controller constants
    p = 0.47
    # i = 0.7474
    i = 0.75
    d = 0.0742
    # p = 0.5


    data_pith_yaw = []


    center_data = []
    frame = 0
    sw = True


    prev_time = round(time.time(), 4)
    curr_time = round(time.time(), 4)
    prev_err_x = 0
    prev_err_y = 0
    sum_err_x_area = 0
    sum_err_y_area = 0
    accelerater_x = 0
    accelerater_y = 0
    avg_diff_time = 0
    # loop การทำงานของหุ่น
    while True:
        frame += 1
        # sw = sw if frame % 200 else not sw
        # center_x = 1280 * (0.25 if sw else 0.75)
        # center_data = center_data.append(center_x)
        # center_y = 720 * (1/4 if frame % 200 else 3/4)
        if len(markers) != 0:  # target found
            x, y = markers[-1].center


            err_x = (
                center_x - x
            )
            err_y = (
                center_y - y
            )
           
            curr_time = round(time.time(), 4)
            diff_time = curr_time - prev_time
            print(F"current: {curr_time} - {round(diff_time, 4)}")
            prev_time = curr_time
            prev_err_x = err_x
            prev_err_y = err_y
           
            if diff_time > 0:
                #derivative part
                accelerater_x = (err_x - prev_err_x) / diff_time
                accelerater_y = (err_y - prev_err_y) / diff_time
                avg_diff_time = (avg_diff_time + diff_time) / 2
           
            #integate part
            sum_err_x_area = sum_err_x_area + (err_x * diff_time)
            sum_err_y_area = sum_err_y_area + (err_y * diff_time)


            # print(F"sum {sum_err_x_area} I {i} err_x {err_x} dT {diff_time} prev_time {prev_time} curr_time {curr_time}")




            if count > 1:
                speed_x = (
                    (p * err_x) +
                    (i * sum_err_x_area) +
                    (d * accelerater_x)
                )


                speed_y = (
                    0
                )


               
                # หมุน gimbal ตามความเร็วที่คำนวณมาก
                ep_gimbal.drive_speed(pitch_speed=speed_y, yaw_speed=-speed_x)


                # เก็บค่ามุมของ gimbal, error x, error y, speed x, speed y
                data_pith_yaw.append(
                    list(list_of_data)
                    + [err_x, err_y, round(-speed_x, 3), round(speed_y, 3), center_x, x]
                )
            # print(F"SX: {speed_x} SY: {speed_y}")
            count += 1


        else:
            # หมุนกลับ center
            ep_gimbal.drive_speed(pitch_speed=0, yaw_speed=0)


        # อ่านภาพ
        img = ep_camera.read_cv2_image(strategy="newest", timeout=0.5)


       
        # วาดสี่เหลี่ยมบนภาพในตำแหน่งที่เจอป้าย
        for j in range(0, len(markers)):
            cv2.rectangle(img, markers[j].pt1, markers[j].pt2, (0, 255, 0))
            cv2.putText(
                img,
                markers[j].text,
                markers[j].center,
                cv2.FONT_HERSHEY_SIMPLEX,
                1.5,
                (0, 255, 0),
                3,
            )
            cv2.putText(
                img,
                str(frame % 200),
                (10, 25),
                cv2.FONT_HERSHEY_SIMPLEX,
                1.5,
                (0, 255, 0),
                3,
            )
        # แสดงภาพ
        cv2.imshow("Markers", img)
        # สำหรับออกจาก loop while
        if cv2.waitKey(1) & 0xFF == ord("q"):
            print(avg_diff_time)
            break


    cv2.destroyAllWindows()


    result = ep_vision.unsub_detect_info(name="marker")
    ep_camera.stop_video_stream()
    ep_robot.close()


    # plot error x, error y, speed x, speed y
    x_point = [i for i in range(len(data_pith_yaw))]
    y_point4 = [i[4] for i in data_pith_yaw]
    y_point5 = [i[5] for i in data_pith_yaw]
    y_point6 = [i[6] for i in data_pith_yaw]
    y_point7 = [i[7] for i in data_pith_yaw]
    y_point8 = [i[8] for i in data_pith_yaw]
    y_point9 = [i[9] for i in data_pith_yaw]


    plt.plot(x_point, y_point8)
    plt.plot(x_point, y_point9)
    # plt.plot(x_point, y_point4)
    # plt.plot(x_point, y_point5)
    # plt.plot(x_point, y_point6)
    # plt.plot(x_point, y_point7)
    plt.legend(["certer_x", "x"])
    plt.show()
    df = pd.DataFrame({"index": x_point, "center_x": y_point8, "e x": y_point4, "e y": y_point5, "u x": y_point6, "u y": y_point7, "x": y_point9})
    df.to_csv("data_0_1.csv")
