import robomaster
from robomaster import robot
import time
import matplotlib.pyplot as plt

adc_l = None
adc_r = None
MAX_SPEED = 2
WALL_DISTANCE_THRESHOLD = 12
count = 0
speed = 30

# ตัวแปรเก็บข้อมูลระยะทางจากเซ็นเซอร์ ToF และสถานะการตรวจจับวัตถุ
tof_distance = 0

# ตัวแปรเก็บข้อมูลระยะทางล่าสุดที่คำนวณได้จากเซ็นเซอร์ซ้ายและขวา (Sharp Sensors)
adc_r_new = 0
adc_l_new = 0

# ลิสต์สำหรับเก็บข้อมูลระยะทางจากเซ็นเซอร์ซ้ายและขวาในแต่ละช่วงเวลา
left_data = []
right_data = []
left_time_data = []
right_time_data = []

# ลิสต์สำหรับเก็บข้อมูลตำแหน่ง x และ y ของหุ่นยนต์
x_positions = [0]
y_positions = [0]

def tof_data_handler(sub_info):
    global tof_distance, status_tof, adc_r, adc_l, adc_r_new, adc_l_new, status_ss_r, status_ss_l
    tof_distance = sub_info[0]
    status_tof = tof_distance < 250

    adc_r = ep_sensor_adaptor.get_adc(id=2, port=1)
    adc_r_cm = (adc_r * 3) / 1023  # process to cm unit
    adc_l = ep_sensor_adaptor.get_adc(id=1, port=2)
    adc_l_cm = (adc_l * 3) / 1023  # process to cm unit

    if adc_r_cm > 1.4:
        adc_r_new = ((adc_r_cm - 4.2) / -0.31) - 3
    elif 1.4 >= adc_r_cm >= 0.6:
        adc_r_new = ((adc_r_cm - 2.03) / -0.07) - 3
    elif 0 <= adc_r_cm < 0.6:
        adc_r_new = ((adc_r_cm - 0.95) / -0.016) - 3

    if adc_l_cm > 1.4:
        adc_l_new = ((adc_l_cm - 4.2) / -0.31) - 3
    elif 1.4 >= adc_l_cm >= 0.6:
        adc_l_new = ((adc_l_cm - 2.03) / -0.07) - 3
    elif 0 <= adc_l_cm < 0.6:
        adc_l_new = ((adc_l_cm - 0.95) / -0.016) - 3

    status_ss_r = 29 > adc_r_new > 2
    status_ss_l = 29 > adc_l_new > 2

def update_position(x_delta, y_delta):
    x_positions.append(x_positions[-1] + x_delta)
    y_positions.append(y_positions[-1] + y_delta)

if __name__ == "__main__":
    ep_robot = robot.Robot()
    print("Initializing robot...")
    ep_robot.initialize(conn_type="ap")
    time.sleep(2)

    ep_sensor = ep_robot.sensor
    ep_chassis = ep_robot.chassis
    ep_gimbal = ep_robot.gimbal
    ep_sensor_adaptor = ep_robot.sensor_adaptor

    ep_sensor.sub_distance(freq=10, callback=tof_data_handler)

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
                if status_tof and status_ss_r and status_ss_l:
                    if tof_distance < 200:
                        ep_chassis.move(x=-0.2, y=0, z=0, xy_speed=MAX_SPEED).wait_for_completed()
                        update_position(-0.2, 0)

                    ep_chassis.drive_wheels(w1=0, w2=0, w3=0, w4=0)
                    time.sleep(0.2)
                    print("Turn Back")
                    ep_chassis.move(x=0, y=0, z=180, xy_speed=MAX_SPEED).wait_for_completed()

                elif status_tof and status_ss_r and not status_ss_l:
                    ep_chassis.drive_wheels(w1=0, w2=0, w3=0, w4=0)
                    print("Turn Left")
                    ep_chassis.move(x=0.15, y=0, z=0, xy_speed=MAX_SPEED).wait_for_completed()
                    update_position(0.15, 0)
                    time.sleep(0.2)
                    ep_chassis.move(x=0, y=0, z=90, xy_speed=MAX_SPEED).wait_for_completed()

                elif status_tof and not status_ss_r:
                    ep_chassis.drive_wheels(w1=0, w2=0, w3=0, w4=0)
                    print("Turn Right")
                    ep_chassis.move(x=0.15, y=0, z=0, xy_speed=MAX_SPEED).wait_for_completed()
                    update_position(0.15, 0)
                    time.sleep(0.2)
                    ep_chassis.move(x=0, y=0, z=-90, xy_speed=MAX_SPEED).wait_for_completed()

                elif not status_tof and status_ss_r:
                    print("Drive forward")
                    ep_chassis.drive_wheels(w1=50, w2=50, w3=50, w4=50)

                    if adc_l_new < WALL_DISTANCE_THRESHOLD:
                        print("Move right")
                        ep_chassis.drive_wheels(w1=-speed, w2=speed, w3=-speed, w4=speed)
                    elif adc_r_new < WALL_DISTANCE_THRESHOLD:
                        print("Move left")
                        ep_chassis.drive_wheels(w1=speed, w2=-speed, w3=speed, w4=-speed)

                elif not status_tof and not status_ss_r:
                    ep_chassis.drive_wheels(w1=0, w2=0, w3=0, w4=0)
                    print("Turn Right")
                    ep_chassis.move(x=0.15, y=0, z=0, xy_speed=MAX_SPEED).wait_for_completed()
                    update_position(0.15, 0)
                    time.sleep(0.2)
                    ep_chassis.move(x=0, y=0, z=-90, xy_speed=MAX_SPEED).wait_for_completed()

            # วาดเส้นทางเมื่อจบรอบ
            plt.plot(x_positions, y_positions, marker='o')
            plt.title(f"Robot Path after round {count}")
            plt.xlabel("X Position (m)")
            plt.ylabel("Y Position (m)")
            plt.grid(True)
            plt.show()

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
