import robomaster
from robomaster import robot
import time

tof_distance = None
adc = None
MAX_SPEED = 0.5  # ลดความเร็วลงเพื่อความแม่นยำ
WALL_DISTANCE_THRESHOLD = 15  # ปรับระยะห่างจากกำแพงให้เหมาะสม
FRONT_DISTANCE_THRESHOLD = 300  # ระยะห่างด้านหน้าที่ต้องการ


def tof_data_handler(sub_info):
    global tof_distance, status_tof
    tof_distance = sub_info[0]
    if 100 < tof_distance < 300: #ก่อนแก้ 100-200
        status_tof = True
    else:
        status_tof = False

    global adc, status_ss_l, status_ss_r, adc_cm
    adc_left = ep_sensor_adaptor.get_adc(id=1, port=2)
    adc_rigth = ep_sensor_adaptor.get_adc(id=2, port=1)
    lst_adc = [adc_left,adc_rigth]
    res = []
    for i in lst_adc:
        adc_to_cm = (i * 3) / 1023
        if adc_to_cm >= 1.4 :
            adc_cm = ((adc_to_cm - 4.169)/-0.308)-1
        
        elif adc_to_cm >= 0.8 :
            adc_cm = ((adc_to_cm - 2.171)/-0.086)-2
        
        elif adc_to_cm >= 0.5 :
            adc_cm = ((adc_to_cm - 1.48)/-0.043)-2
        
        elif adc_to_cm >= 0.31 :
            adc_cm = ((adc_to_cm - 0.95)/-0.016)-8
        res.append(adc_cm)
        
    #print("dis", res, "cm")

    if 25 > res[0] > 2: # ก่อนแก้ 20-5 
        status_ss_l = True
    else:
        status_ss_l = False
    if 25 > res[1] > 2: # ก่อนแก้ 20-5 
        status_ss_r = True
    else:
        status_ss_r = False

    print(f"{res[0]:.2f} {res[1]:.2f} cm  ToF {status_tof}  Left {status_ss_l}  Rigth {status_ss_r}")
    


if __name__ == "__main__":
    ep_robot = robot.Robot()
    ep_robot.initialize(conn_type="ap")

    ep_sensor = ep_robot.sensor
    ep_chassis = ep_robot.chassis
    ep_gimbal = ep_robot.gimbal
    ep_sensor_adaptor = ep_robot.sensor_adaptor

    ep_sensor.sub_distance(freq=10, callback=tof_data_handler)
    ep_gimbal.recenter(pitch_speed=200, yaw_speed=200).wait_for_completed()

    while True:
        if tof_distance is None or adc_l is None or adc_r is None:
            print("Waiting the sensor...")
            time.sleep(1)
            continue
        if tof_distance < 100 :
            ep_chassis.drive_wheels(w1=0, w2=0, w3=0, w4=0)
            time.sleep(0.5)
            ep_chassis.drive_wheels(w1=-15, w2=-15, w3=-15, w4=-15)
            time.sleep(0.5)
        
        if status_tof == False and status_ss_r == True:
            print("Drive Forward")
            ep_chassis.drive_wheels(w1=50, w2=50, w3=50, w4=50)

        if status_tof == True and status_ss_r == True and status_ss_l == True:
            time.sleep(0.2)
            ep_chassis.drive_wheels(w1=0, w2=0, w3=0, w4=0)
            time.sleep(0.5)
            print("Turn Back")
            ep_chassis.move(x=0, y=0, z=-180, z_speed=100).wait_for_completed()
            ep_gimbal.recenter(pitch_speed=200, yaw_speed=200).wait_for_completed()
            time.sleep(0.5)
            ep_chassis.move(x=0.5, y=0, z=0, xy_speed=MAX_SPEED).wait_for_completed()
            time.sleep(0.5)

        if status_tof == True and status_ss_r == True and status_ss_l == False:
            time.sleep(0.2)
            ep_chassis.drive_wheels(w1=0, w2=0, w3=0, w4=0)
            time.sleep(0.5)
            print("Turn Left")
            ep_chassis.move(x=0, y=0, z=90, z_speed=100).wait_for_completed()
            ep_gimbal.recenter(pitch_speed=200, yaw_speed=200).wait_for_completed()
            time.sleep(0.5)
            ep_chassis.move(x=0.5, y=0, z=0, xy_speed=MAX_SPEED).wait_for_completed()
            time.sleep(0.5)

        if status_ss_r == False:
            time.sleep(0.2)            
            ep_chassis.drive_wheels(w1=0, w2=0, w3=0, w4=0)
            time.sleep(0.5)
            print("Turn Right")
            ep_chassis.move(x=0, y=0, z=-90, z_speed=100).wait_for_completed()
            ep_gimbal.recenter(pitch_speed=200, yaw_speed=200).wait_for_completed()
            time.sleep(0.5)
            ep_chassis.move(x=0.5, y=0, z=0, xy_speed=MAX_SPEED).wait_for_completed()
            time.sleep(0.5)