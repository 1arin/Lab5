import robomaster
from robomaster import robot
import time
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import csv

MAX_SPEED = 0.5
WALL_DISTANCE_THRESHOLD = 12
FRONT_WALL_THRESHOLD = 350 # มิลลิลิตร
count = 0
speed = 30

# ตัวแปรเก็บข้อมูลระยะทาง
tof_distance = None
adc_r_new = None
adc_l_new = None
axis_x = []
axis_y = []
# time_data = []
tof_data = []
sharp_left_data = []
sharp_right_data = []
chasis_data = []

def sub_position_handler(position_info):
    x, y, z = position_info
    axis_x.append(x)
    axis_y.append(y)
    chasis_data.append((x, y, z)) 

def sharp_left_right(left, right):
    S_l = left
    s_r = right
    sharp_right_data.append(s_r); sharp_left_data.append(S_l)

def chassis(chassis_info):
    chassis_position = chassis_info
    chasis_data.append(chassis_position)

def tof_data_handler(sub_info):
    global tof_distance, status_tof, adc_r_new, adc_l_new, status_ss_r, status_ss_l, adc_r,adc_l
    tof_distance = sub_info[0]
    tof_data.append(tof_distance)

    print(f"ToF distance received: {tof_distance} mm")

    if tof_distance < 250:
        status_tof = True
    else:
        status_tof = False
    

    adc_r = ep_sensor_adaptor.get_adc(id=2, port=1)
    adc_r_cm = (adc_r * 3) / 1023  # process to cm unit
    adc_l = ep_sensor_adaptor.get_adc(id=1, port=2)
    adc_l_cm = (adc_l * 3) / 1023  # process to cm unit
        
    if adc_l_cm > 1.4:
        adc_l_new = ((adc_l_cm - 4.2) / -0.31)-3 
    elif 1.4 >= adc_l_cm >= 0.6:
        adc_l_new = ((adc_l_cm - 2.03) / -0.07)-3 
    elif 0 <= adc_l_cm < 0.6:
        adc_l_new = ((adc_l_cm - 0.95) / -0.016)-3

    sharp_right_data.append(adc_r_new)
    sharp_left_data.append(adc_l_new)

    print(f"Filtered Right Distance: {adc_r_new} cm")
    print(f"Filtered Left Distance: {adc_l_new} cm")

    filtered_tof, filtered_left, filtered_right, filtered_chassis = filter_signal(
        tof_distance, adc_l_new, adc_r_new, chasis_data[-1] if chasis_data else (0, 0, 0)
    )
    
    sharp_right_data.append(filtered_right)
    sharp_left_data.append(filtered_left)
    tof_data.append(filtered_tof)
    chasis_data.append(filtered_chassis)
        
    # print(f"distance from front wall:right  {adc_r} left  {adc_l}")
    # print(f"distance from front wall: right  {adc_r_new} left  {adc_l_new}")

    if 18 > adc_r_new > 5:
        status_ss_r = True
    else:
        status_ss_r = False

    if 29 > adc_l_new > 2:
        status_ss_l = True
    else:
        status_ss_l = False

    

    print("status tof = {} and status right = {}".format(status_tof,status_ss_r))
    print('distance from right wall = {} cm'.format(adc_r_new))
    print('distance from left wall = {} cm'.format(adc_l_new))
    print('chassis x= {} and chassis y = {} '.format(chasis_data[0],chasis_data[1]))

    # headers = ['Left Sharp', 'Right Sharp', 'TOF', 'Chassis X', 'Chassis Y', 'Chassis Z']
    # file_name = 'sensor_data.csv'

    # with open(file_name, 'w', newline='', encoding='utf-8') as file:
    #     writer = csv.writer(file)
    #     writer.writerow(headers)
        
    #     # สร้าง zip object เพื่อรวมข้อมูลจากทุก list ให้อยู่ในแถวเดียวกัน
    #     for row in zip(sharp_left_data, sharp_right_data, tof_data, 
    #                 [x[0] for x in chasis_data], 
    #                 [x[1] for x in chasis_data], 
    #                 [x[2] for x in chasis_data]):
    #         writer.writerow(row)

def plot_graphs():
    fig, axs = plt.subplots(2, 2, figsize=(10, 8))
    
    # กราฟที่ 1
    axs[0, 0].plot(sharp_left_data, 'r')
    axs[0, 0].set_title('Left Sharp')
    axs[0, 0].set_ylabel('Distance (cm)')

    # กราฟที่ 2
    axs[0, 1].plot(sharp_right_data, 'g')
    axs[0, 1].set_title('Right Sharp')
    axs[0, 1].set_ylabel('Distance (cm)')

    # กราฟที่ 3
    axs[1, 0].plot(tof_data, 'b')
    axs[1, 0].set_title('TOF')
    axs[1, 0].set_ylabel('Distance (mm)')

    # กราฟที่ 4
    x_pos = [pos[0] for pos in chasis_data]
    y_pos = [pos[1] for pos in chasis_data]
    axs[1, 1].plot(x_pos, y_pos, 'y')
    axs[1, 1].set_title('Chassis Position')
    axs[1, 1].set_xlabel('X Position')
    axs[1, 1].set_ylabel('Y Position')

    # ปรับระยะห่างระหว่าง subplot
    plt.tight_layout()

    # แสดงกราฟ
    plt.show()

    # เพิ่มการพล็อตเส้นทางการเคลื่อนที่ของหุ่นยนต์
    plt.figure(figsize=(10, 5))
    plt.plot(axis_x, axis_y, label='Path', marker='o')
    plt.title('Robot Movement Path')
    plt.xlabel('X Position')
    plt.ylabel('Y Position')
    plt.legend()
    plt.grid(True)
    plt.show()  

def filter_signal(r,l,tof,chassis):
    all_sensor = [tof_data,sharp_left_data,sharp_right_data,chasis_data]
    sen = [tof,l,r,chassis]
    res = []

    for i in range(len(sen)):
        if len(all_sensor[i]) > 0:
            yn = sen[i] + (0.65 * all_sensor[i][-1])
        else:
            yn = sen[i]

        res.append(yn)
    return res[0],res[1],res[2],res[3]


if __name__ == "__main__":
    # เริ่มต้นการทำงานของหุ่นยนต์
    ep_robot = robot.Robot()
    print("Initializing robot...")
    ep_robot.initialize(conn_type="ap")
    time.sleep(2)  # รอ 2 วินาทีหลังการเชื่อมต่อ

    # เริ่มต้นการทำงานของเซ็นเซอร์ต่าง ๆ
    ep_sensor = ep_robot.sensor
    ep_chassis = ep_robot.chassis
    ep_gimbal = ep_robot.gimbal
    ep_sensor_adaptor = ep_robot.sensor_adaptor

    # สมัครสมาชิกฟังก์ชัน callback เพื่อรับข้อมูลจากเซ็นเซอร์ ToF และ Sharp Sensors
    ep_sensor.sub_distance(freq=60, callback=tof_data_handler)
    ep_chassis.sub_position(freq=60, callback=sub_position_handler)
    ep_gimbal.recenter().wait_for_completed()

    program_finished = False

    try:
        while True:
            if tof_distance is None or adc_l is None or adc_r is None:
                print("Waiting for sensor data...")
                time.sleep(1)
                continue
                
            while status_tof == False and status_ss_r == True:
                    # print("Drive forward")
                    ep_chassis.drive_wheels(w1=50, w2=50, w3=50, w4=50)

                    if axis_x[-1] < 0 and count == 1:
                        print("first axis_x",axis_x[0])
                        print("last axis_x",axis_x[-1])
                        ep_chassis.drive_speed(x=0, y=0, z=0, timeout=0.75)
                        time.sleep(1)
                        break
            
            gap = (WALL_DISTANCE_THRESHOLD - adc_r_new) / 100

            if abs(axis_x[-1] - axis_x[0]) < 0.05:
                break

            if status_ss_r == False and status_tof == False :
                ep_chassis.move(x=0,y=-gap,z=0).wait_for_completed()
                
            if status_tof == True and status_ss_r == True and status_ss_l == True:
                if tof_distance <200:
                    ep_chassis.move(x=-0.2, y=0, z=0, xy_speed=MAX_SPEED).wait_for_completed()
                    ep_chassis.drive_speed(x=0, y=0, z=0, timeout=0.75)
                    time.sleep(1)
                    print("Turn Back")
                    ep_chassis.move(x=0, y=0, z=180, xy_speed=MAX_SPEED).wait_for_completed()
                    time.sleep(0.2)
                    count += 1
    
    except KeyboardInterrupt:
        print("Program stopped by user")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        print("Cleaning up...")
        ep_sensor.unsub_distance()
        ep_robot.close()
        print("Program ended.")

        # plt.figure(figsize=(10, 5))
        # plt.plot(axis_x, axis_y, label='Path', marker='o')
        # plt.title('Robot Movement Path')
        # plt.xlabel('X Position')
        # plt.ylabel('Y Position')
        # plt.legend()
        # plt.grid(True)
        # plt.show()
        plot_graphs()

        tof_df = pd.DataFrame({'TOF Distance (mm)': tof_distance})
        tof_df.to_csv('tof_data.csv', index=False)
        
        # สร้าง DataFrame สำหรับข้อมูล Sharp Left และ Right
        sharp_df = pd.DataFrame({
            'Sharp Left Distance (cm)': adc_l_new,
            'Sharp Right Distance (cm)': adc_r_new
        })
        sharp_df.to_csv('sharp_data.csv', index=False)

        # สร้าง DataFrame สำหรับข้อมูล Chassis Position
        chassis_df = pd.DataFrame({
            'X Position': chasis_data[0],
            'Y Position': chasis_data[1]
        })
        chassis_df.to_csv('chassis_data.csv', index=False)