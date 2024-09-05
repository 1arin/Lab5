import robomaster
from robomaster import robot
import time
import matplotlib.pyplot as plt
import numpy as np

MAX_SPEED = 0.5
WALL_DISTANCE_THRESHOLD = 12
FRONT_WALL_THRESHOLD = 250  # มิลลิเมตร
count = 0
speed = 30

# ตัวแปรเก็บข้อมูลระยะทาง
tof_distance = 0
adc_r_new = 0
adc_l_new = 0
axis_x = []
axis_y = []
# time_data = []
tof_data = []
sharp_left_data = []
sharp_right_data = []
chasis_data = []

def sub_position_handler(position_info):
    x, y, z = position_info
    axis_x.append(x); axis_y.append(y) 

def sharp_left_rigth(left, rigth):
    S_l = left
    s_r = rigth
    sharp_right_data.append(s_r); sharp_left_data.append(S_l)

def tof(tof_info):
    tof_sensor_data = tof_info
    tof_data.append(tof_sensor_data)

def chassis(chassis_info):
    chassis_position = chassis_info
    chasis_data.append(chassis_position)

def tof_data_handler(sub_info):
    global tof_distance, status_tof
    tof_distance = sub_info[0]
    if tof_distance < 250:
        status_tof = True
    else:
        status_tof = False
    print(f"ToF distance: {tof_distance} mm")

    global adc_r,adc_l,adc_r_new,adc_l_new,status_ss_r,status_ss_l
    adc_r = ep_sensor_adaptor.get_adc(id=2, port=1)

    adc_r_cm = (adc_r * 3) / 1023  # process to cm unit
    adc_l = ep_sensor_adaptor.get_adc(id=1, port=2)
    adc_l_cm = (adc_l * 3) / 1023  # process to cm unit

    if adc_r_cm > 1.4:
        adc_r_new = ((adc_r_cm - 4.2) / -0.31)-3
    elif 1.4 >= adc_r_cm >= 0.6:
        adc_r_new = ((adc_r_cm - 2.03) / -0.07)-3
    elif 0 <= adc_r_cm < 0.6:
        adc_r_new = ((adc_r_cm - 0.95) / -0.016)-3
        
    if adc_l_cm > 1.4:
        adc_l_new = ((adc_l_cm - 4.2) / -0.31)-3 
    elif 1.4 >= adc_l_cm >= 0.6:
        adc_l_new = ((adc_l_cm - 2.03) / -0.07)-3 
    elif 0 <= adc_l_cm < 0.6:
        adc_l_new = ((adc_l_cm - 0.95) / -0.016)-3
        
    # print(f"distance from front wall:right  {adc_r} left  {adc_l}")
    print(f"distance from front wall: right  {adc_r_new} left  {adc_l_new}")

    if 29 > adc_r_new > 2:
        status_ss_r = True
    else:
        status_ss_r = False

    if 29 > adc_l_new > 2:
        status_ss_l = True
    else:
        status_ss_l = False

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
    ep_sensor.sub_distance(freq=10, callback=tof_data_handler)
    ep_chassis.sub_position(freq=50, callback=sub_position_handler)
    # ep_sensor_adaptor.sub_adapter(freq=5, callback=sub_data_handler)


    # ปรับตำแหน่ง Gimbal ให้ตรงศูนย์
    ep_gimbal.recenter().wait_for_completed()

    try:
        while True:
            if tof_distance is None or adc_l is None or adc_r is None:
                print("Waiting for sensor data...")
                time.sleep(1)
                continue
            
            # คำนวณความแตกต่างระหว่างระยะห่างปัจจุบันกับระยะห่างที่ต้องการ
            y_speed = WALL_DISTANCE_THRESHOLD - adc_r_new
            
            # คำนวณความเร็วในการปรับตำแหน่งทางด้านข้าง
            
            if status_tof == False:  # ถ้าไม่มีกำแพงด้านหน้า
                if abs(y_speed) > 1:  # ถ้าความคลาดเคลื่อนมากกว่า 1 ซม.
                    # เคลื่อนที่ไปข้างหน้าพร้อมปรับตำแหน่งทางด้านข้าง
                    ep_chassis.drive_speed(x=MAX_SPEED, y=y_speed, z=0)
                else:
                    # เคลื่อนที่ไปข้างหน้าตรงๆ
                    ep_chassis.drive_speed(x=MAX_SPEED, y=0, z=0)
            else:
                # ถ้าเจอกำแพงด้านหน้า ให้หยุดและหมุน 180 องศา
                ep_chassis.drive_speed(x=0, y=0, z=0)
                print("Front wall detected. Turning around...")
                ep_chassis.move(x=0, y=0, z=180, z_speed=90).wait_for_completed()
            
            print(f"Current distance from wall: {adc_r_new:.2f} cm")
            time.sleep(0.1)  # หน่วงเวลาเล็กน้อยเพื่อลดการใช้ CPU

    except KeyboardInterrupt:
        print("Program stopped by user")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        print("Cleaning up...")
        ep_sensor.unsub_distance()
        ep_chassis.drive_speed(x=0, y=0, z=0)
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

    fig, axs = plt.subplots(2, 2, figsize=(10, 8))
    # กราฟที่ 1
    axs[0, 0].plot(sharp_left_data, 'r')
    axs[0, 0].set_title('Left Sharp')

    # กราฟที่ 2
    axs[0, 1].plot(sharp_right_data, 'g')
    axs[0, 1].set_title('Rigth Sharp')

    # กราฟที่ 3
    axs[1, 0].plot(tof_data, 'b')
    axs[1, 0].set_title('TOF')

    # กราฟที่ 4
    axs[1, 1].plot(chasis_data, 'y')
    axs[1, 1].set_title('Chassis')

    # ปรับระยะห่างระหว่าง subplot
    plt.tight_layout()

    # แสดงกราฟ
    plt.show()