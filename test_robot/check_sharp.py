import robomaster
from robomaster import robot
import time

MAX_SPEED = 1
WALL_DISTANCE_THRESHOLD = 200

def tof_data_handler(sub_info):
    global tof_distance, status_tof
    tof_distance = sub_info[0]
    if 300 < tof_distance < 650:
        status_tof = True
    else:
        status_tof = False
    print(f"ToF distance: {tof_distance} mm")

    global adc_r,adc_l,adc_r_new,adc_l_new
    adc_r = ep_sensor_adaptor.get_adc(id=2, port=2)
    adc_r_cm = (adc_r * 3) / 1023  # process to cm unit
    adc_l = ep_sensor_adaptor.get_adc(id=1, port=1)
    adc_l_cm = (adc_l * 3) / 1023  # process to cm unit

    if adc_r_cm > 1.4:
        adc_r_new = ((adc_r_cm - 4.2) / -0.31)-5
    elif 1.4 >= adc_r_cm >= 0.6:
        adc_r_new = ((adc_r_cm - 2.03) / -0.07)-5
    elif 0 <= adc_r_cm < 0.6:
        adc_r_new = ((adc_r_cm - 0.95) / -0.016)-5

    if adc_l_cm > 1.4:
        adc_l_new = ((adc_l_cm - 4.2) / -0.31)-5
    elif 1.4 >= adc_l_cm >= 0.6:
        adc_l_new = ((adc_l_cm - 2.03) / -0.07)-5
    elif 0 <= adc_l_cm < 0.6:
        adc_l_new = ((adc_l_cm - 0.95) / -0.016)-5

    # print(f"distance from front wall:right  {adc_r} left  {adc_l}")
    print(f"distance from front wall:right  {adc_r_new} left  {adc_l_new}")

    # if 16.5 > adc_cm > 5.5:
    #     status_ss_1 = True
    # else:
    #     status_ss_1 = False
    # # print(f"ToF distance: {adc_1} mm")
    # print(f"status_tof {status_tof} , status_ss_1 {status_ss_1}")
    # time.sleep(1)


print("****************************")

if __name__ == "__main__":
    ep_robot = robot.Robot()
    print("Initializing robot...")
    ep_robot.initialize(conn_type="ap")
    time.sleep(2)  # รอ 2 วินาทีหลังการเชื่อมต่อ
    ep_sensor = ep_robot.sensor
    ep_chassis = ep_robot.chassis
    ep_gimbal = ep_robot.gimbal
    ep_sensor_adaptor = ep_robot.sensor_adaptor
    ep_sensor.sub_distance(freq=10, callback=tof_data_handler)
    ep_gimbal.recenter().wait_for_completed()
    # while True:
    #     if adc_r_new > 0 and adc_l_new < 0:
    #         ep_chassis.move(x=0, y=0, z=90, xy_speed=MAX_SPEED).wait_for_completed()
    #         ep_gimbal.recenter().wait_for_completed()
    #         time.sleep(1)
            
        
    #     elif adc_l_new >0 and adc_r_new < 0:
    #         ep_chassis.move(x=0, y=0, z=-90, xy_speed=MAX_SPEED).wait_for_completed()
    #         ep_gimbal.recenter().wait_for_completed()
    #         time.sleep(1)
        
    #     elif adc_l_new<0 and adc_r_new<0 and tof_distance<0:
    #         ep_chassis.move(x=0, y=0, z=-180, xy_speed=MAX_SPEED).wait_for_completed()
    #         ep_gimbal.recenter().wait_for_completed()
    #         time.sleep(1)
        
    #     elif adc_l_new>0 and adc_r_new>0 and tof_distance <0:
    #         ep_chassis.move(x=0, y=0, z=-180, xy_speed=MAX_SPEED).wait_for_completed()
    #         ep_gimbal.recenter().wait_for_completed()
    #         time.sleep(1)




    # ep_sensor.unsub_distance()
    # ep_sensor.unsub_adapter()
    # ep_chassis.drive_speed(x=0, y=0, z=0)
    # ep_robot.close()
    # print("Program ended.")c

    