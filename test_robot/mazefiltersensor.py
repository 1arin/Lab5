import robomaster
from robomaster import robot
import time

adc_l = None
adc_r = None
MAX_SPEED = 2
WALL_DISTANCE_THRESHOLD = 12
count = 0
speed = 30

# ตัวแปรเก็บข้อมูลระยะทางจากเซ็นเซอร์ ToF และสถานะการตรวจจับวัตถุ
tof_distance = 0
# status_tof = False
# ตัวแปรเก็บข้อมูลระยะทางล่าสุดที่คำนวณได้จากเซ็นเซอร์ซ้ายและขวา (Sharp Sensors)
adc_r_new = 0
adc_l_new = 0
# ลิสต์สำหรับเก็บข้อมูลระยะทางจากเซ็นเซอร์ซ้ายและขวาในแต่ละช่วงเวลา
left_data = []
right_data = []
left_time_data = []
right_time_data = []
adc_l_filtered = 0
adc_r_filtered = 0

def filter_signal(sen_l, sen_r):
    global adc_l_filtered, adc_r_filtered
    all_sensor = [adc_l_filtered, adc_r_filtered]
    sen = [sen_l, sen_r]
    res = []
    for i in range(len(sen)):
        yn = sen[i] + (0.65 * all_sensor[i])
        res.append(yn)
    return res[0], res[1]


def tof_data_handler(sub_info):
    global tof_distance, status_tof, adc_r, adc_l, adc_r_new, adc_l_new, status_ss_r, status_ss_l, adc_l_filtered, adc_r_filtered
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

    adc_l_filtered, adc_r_filtered = filter_signal(adc_l_new, adc_r_new)

        
    # print(f"distance from front wall:right  {adc_r} left  {adc_l}")
    print(f"Filtered distance from front wall: right {adc_r_filtered:.2f} left {adc_l_filtered:.2f}")

    if 29 > adc_r_filtered > 2:
        status_ss_r = True
    else:
        status_ss_r = False

    if 29 > adc_l_filtered > 2:
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
    # ep_sensor_adaptor.sub_adapter(freq=5, callback=sub_data_handler)


    # ปรับตำแหน่ง Gimbal ให้ตรงศูนย์
    ep_gimbal.recenter().wait_for_completed()
    
    try:
        while True:
            count += 1 
            print("current count = {}".format(count))
            

            if tof_distance is None or adc_l is None or adc_r is None:
                print("Waiting for sensor data...")
                time.sleep(1)
                continue

            while True:
                # T T T 1
                if status_tof == True and status_ss_r == True and status_ss_l == True:
                    if tof_distance <200:
                        ep_chassis.move(x=-0.2, y=0, z=0, xy_speed=MAX_SPEED).wait_for_completed()

                    ep_chassis.drive_wheels(w1=0, w2=0, w3=0, w4=0)
                    time.sleep(0.2)
                    print("Turn Back")
                    ep_chassis.move(x=0, y=0, z=180, xy_speed=MAX_SPEED).wait_for_completed()
                    ep_gimbal.recenter(pitch_speed=200, yaw_speed=200).wait_for_completed()
                    time.sleep(0.2)

                    # recenter
                    if adc_l_new < WALL_DISTANCE_THRESHOLD:
                        print("Move right")
                        ep_chassis.drive_wheels(w1=-speed, w2=speed, w3=-speed, w4=speed)
                    elif adc_r_new < WALL_DISTANCE_THRESHOLD:
                        print("Move left")
                        ep_chassis.drive_wheels(w1=speed, w2=-speed, w3=speed, w4=-speed)

                # T T F 2
                elif status_tof == True and status_ss_r == True and status_ss_l == False:
                    ep_chassis.drive_wheels(w1=0, w2=0, w3=0, w4=0)
                    print("Turn Left")
                    ep_chassis.move(x=0.15, y=0, z=0, xy_speed=MAX_SPEED).wait_for_completed()
                    time.sleep(0.2)
                    ep_chassis.move(x=0, y=0, z=90, xy_speed=MAX_SPEED).wait_for_completed()
                    ep_gimbal.recenter(pitch_speed=200, yaw_speed=200).wait_for_completed()
                    ep_chassis.move(x=0.3, y=0, z=0, xy_speed=MAX_SPEED).wait_for_completed()
                    time.sleep(0.2)

                    if tof_distance <200:
                        ep_chassis.move(x=-0.2, y=0, z=0, xy_speed=MAX_SPEED).wait_for_completed()
                        time.sleep(0.2)

                # T F 3
                elif status_tof == True and status_ss_r == False:
                    ep_chassis.drive_wheels(w1=0, w2=0, w3=0, w4=0)
                    print("Turn Right")
                    ep_chassis.move(x=0.15, y=0, z=0, xy_speed=MAX_SPEED).wait_for_completed()
                    time.sleep(0.2)
                    ep_chassis.move(x=0, y=0, z=-90, xy_speed=MAX_SPEED).wait_for_completed()
                    ep_gimbal.recenter(pitch_speed=200, yaw_speed=200).wait_for_completed()
                    ep_chassis.move(x=0.3, y=0, z=0, xy_speed=MAX_SPEED).wait_for_completed()
                    time.sleep(0.2)

                    if tof_distance <200:
                        ep_chassis.move(x=-0.2, y=0, z=0, xy_speed=MAX_SPEED).wait_for_completed()
                        time.sleep(0.2)

                # F T 4
                elif status_tof == False and status_ss_r == True:
                    print("Drive forward")
                    ep_chassis.drive_wheels(w1=50, w2=50, w3=50, w4=50)

                    if adc_l_new < WALL_DISTANCE_THRESHOLD:
                        print("Move right")
                        ep_chassis.drive_wheels(w1=-speed, w2=speed, w3=-speed, w4=speed)
                    elif adc_r_new < WALL_DISTANCE_THRESHOLD:
                        print("Move left")
                        ep_chassis.drive_wheels(w1=speed, w2=-speed, w3=speed, w4=-speed)

                # F F 5
                elif status_tof == False and status_ss_r == False:
                    ep_chassis.drive_wheels(w1=0, w2=0, w3=0, w4=0)
                    print("Turn Right")
                    ep_chassis.move(x=0.15, y=0, z=0, xy_speed=MAX_SPEED).wait_for_completed()
                    time.sleep(0.2)
                    ep_chassis.move(x=0, y=0, z=-90, xy_speed=MAX_SPEED).wait_for_completed()
                    ep_gimbal.recenter(pitch_speed=200, yaw_speed=200).wait_for_completed()
                    ep_chassis.move(x=0.3, y=0, z=0, xy_speed=MAX_SPEED).wait_for_completed()
                    time.sleep(0.2)

                    if tof_distance <200:
                        ep_chassis.move(x=-0.2, y=0, z=0, xy_speed=MAX_SPEED).wait_for_completed()
                        time.sleep(0.2)

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