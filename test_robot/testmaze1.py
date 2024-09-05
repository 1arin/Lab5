# เดินในกรอบ 4 เหลี่ยมได้แล้ว

import robomaster
from robomaster import robot
import time

tof_distance = None
adc = None
MAX_SPEED = 0.5  # ลดความเร็วลงเพื่อความแม่นยำ
WALL_DISTANCE_THRESHOLD = 15  # ปรับระยะห่างจากกำแพงให้เหมาะสม
FRONT_DISTANCE_THRESHOLD = 30  # ระยะห่างด้านหน้าที่ต้องการ
LEFT_CHECK_ANGLE = 90
RIGTH_CHECK_ANGLE = -90

def tof_data_handler(sub_info):
    global tof_distance, status_tof, adc, status_ss_1, adc_cm
    tof_distance = sub_info[0]
    status_tof = 50 < tof_distance < 300  # ปรับช่วงการตรวจจับ

    adc = ep_sensor_adaptor.get_adc(id=1, port=2)
    adc_to_cm = (adc * 3) / 1023

    if adc_to_cm > 1.4:
        adc_cm = (adc_to_cm - 4.2) / -0.31
    elif 1.4 >= adc_to_cm >= 0.6:
        adc_cm = (adc_to_cm - 2.03) / -0.07
    else:
        adc_cm = (adc_to_cm - 0.95) / -0.016

    status_ss_1 = FRONT_DISTANCE_THRESHOLD > adc_cm > 5  # ปรับช่วงการตรวจจับ
    print(f"Front distance: {adc_cm:.2f} cm, ToF distance: {tof_distance:.2f} cm")
    print(f"status_tof: {status_tof}, status_ss_1: {status_ss_1}")

def adjust_to_wall():
    global adc_cm
    error = WALL_DISTANCE_THRESHOLD - adc_cm
    kp = 0.01  # ค่า Proportional gain
    adjustment = kp * error
    return max(min(adjustment, MAX_SPEED), -MAX_SPEED)

def check_left_clear():
    """หมุนไปทางซ้ายเพื่อตรวจสอบว่าทางซ้ายว่างหรือไม่"""
    ep_gimbal.move(pitch=0, yaw=-LEFT_CHECK_ANGLE).wait_for_completed()
    time.sleep(0.1)  # หน่วงเวลาเล็กน้อยเพื่อให้การหมุนเสร็จสมบูรณ์
    is_clear = status_tof and (tof_distance > FRONT_DISTANCE_THRESHOLD)
    ep_gimbal.recenter().wait_for_completed()  # หมุนกลับมาที่ตำแหน่งเดิม
    return is_clear

def check_rigth_clear():
    """หมุนไปทางซ้ายเพื่อตรวจสอบว่าทางซ้ายว่างหรือไม่"""
    ep_gimbal.move(pitch=0, yaw=-RIGTH_CHECK_ANGLE).wait_for_completed()
    time.sleep(0.1)  # หน่วงเวลาเล็กน้อยเพื่อให้การหมุนเสร็จสมบูรณ์
    is_clear = status_tof and (tof_distance > FRONT_DISTANCE_THRESHOLD)
    ep_gimbal.recenter().wait_for_completed()  # หมุนกลับมาที่ตำแหน่งเดิม
    return is_clear

if __name__ == "__main__":
    ep_robot = robot.Robot()
    ep_robot.initialize(conn_type="ap")

    ep_sensor = ep_robot.sensor
    ep_chassis = ep_robot.chassis
    ep_gimbal = ep_robot.gimbal
    ep_sensor_adaptor = ep_robot.sensor_adaptor

    ep_sensor.sub_distance(freq=10, callback=tof_data_handler)
    ep_gimbal.recenter().wait_for_completed()

    try:
        while True:
            if tof_distance is None or adc is None:
                print("Waiting for sensor data...")
                time.sleep(0.1)
                continue

            y_speed = adjust_to_wall()

            if status_ss_1 and status_tof:
                if check_left_clear():
                    # หมุนไปทางซ้ายถ้าทางซ้ายว่าง
                    ep_chassis.move(x=0, y=0, z=LEFT_CHECK_ANGLE, xy_speed=MAX_SPEED).wait_for_completed()
                else:
                    # หมุน 90 องศาไปทางขวาถ้าทางซ้ายไม่ว่าง
                    ep_chassis.move(x=0, y=0, z=-90, xy_speed=MAX_SPEED).wait_for_completed()
                ep_gimbal.recenter().wait_for_completed()
            elif status_ss_1 and not status_tof:
                # ชะลอและเคลื่อนที่ไปข้างหน้าช้าๆ เมื่อใกล้สิ่งกีดขวางด้านหน้า
                ep_chassis.move(x=0.1, y=y_speed, z=0, xy_speed=MAX_SPEED/2).wait_for_completed()
            elif not status_ss_1 and (status_tof or adc_cm > 30):
                # เคลื่อนที่ไปข้างหน้าพร้อมปรับแนวขนานกับกำแพง
                if status_tof > 100:
                    ep_chassis.move(x=0.2, y=0, xy_speed=MAX_SPEED).wait_for_completed()
                else:
                    ep_chassis.drive_wheels(w1=-10, w2=-10, w3=-10, w4=-10)

                ep_chassis.move(x=0.15, y=0, z=0 , xy_speed=MAX_SPEED).wait_for_completed()
                ep_chassis.move(x=0, y=0, z=90 , xy_speed=MAX_SPEED).wait_for_completed()
                ep_gimbal.recenter().wait_for_completed()
                ep_chassis.move(x=0.5, y=0, z=0 , xy_speed=MAX_SPEED).wait_for_completed()
            else:
                # หยุดและปรับตำแหน่งเมื่อไม่แน่ใจ
                ep_chassis.drive_speed(x=0, y=0, z=0)

            time.sleep(0.05)  # เพิ่มการหน่วงเวลาเล็กน้อยเพื่อลดการใช้ CPU

    except KeyboardInterrupt:
        print("Program stopped by user")
    finally:
        ep_chassis.drive_speed(x=0, y=0, z=0)  # หยุดการเคลื่อนที่
        ep_sensor.unsub_distance()
        ep_robot.close()