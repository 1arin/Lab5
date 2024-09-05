import time
import matplotlib.pyplot as plt
from robomaster import robot

ep_robot = robot.Robot()
ep_robot.initialize(conn_type="ap")
ep_sensor_adaptor = ep_robot.sensor_adaptor

# TOF sensor และ Sharp sensor
tof_sensor = ep_robot.sensor
sharp_left = ep_sensor_adaptor.get_adc(id=1, port=1)  
sharp_right = ep_sensor_adaptor.get_io(id=1, port=1)

TOF_THRESHOLD = 300  # ระยะห่างในมิลลิเมตรด้านหน้า
SHARP_THRESHOLD = 150  # ระยะห่างจากด้านซ้ายและขวาในมิลลิเมตร
COLLISION_THRESHOLD = 50  # ระยะที่ถือว่าชนผนัง

sub_data = []

# ตัวแปรสำหรับบันทึกเส้นทาง
path = []

def sub_data_handler(sub_info):
    distance = sub_info
    print("tof1:{0}  tof2:{1}  tof3:{2}  tof4:{3}".format(distance[0], distance[1], distance[2], distance[3]))
    sub_data.append((distance[0], distance[1], distance[2], distance[3]))

def get_side_distances():
    left_distance = sharp_left.get_distance()
    right_distance = sharp_right.get_distance()
    return left_distance, right_distance

def check_collision(front, left, right):
    return min(front, left, right) < COLLISION_THRESHOLD

def move_robot():
    start_time = time.time()
    rounds = 0
    round_start_time = start_time
    
    while rounds < 2 and (time.time() - start_time) < 300:  # 5 minutes = 300 seconds
        front_distance = sub_data_handler()
        left_distance, right_distance = get_side_distances()
        
        if check_collision(front_distance, left_distance, right_distance):
            print(f"การชนตรวจพบในรอบที่ {rounds + 1}")
            break
        
        if front_distance < TOF_THRESHOLD:
            ep_robot.chassis.drive_speed(x=0, y=0, z=0)
            if left_distance > right_distance:
                ep_robot.chassis.drive_speed(x=0, y=0, z=-30)  # หมุนไปทางซ้าย
            else:
                ep_robot.chassis.drive_speed(x=0, y=0, z=30)  # หมุนไปทางขวา
        else:
            ep_robot.chassis.drive_speed(x=0.5, y=0, z=0)  # เดินไปข้างหน้า
        
        # บันทึกตำแหน่งปัจจุบัน
        # ตัวอย่างนี้แสดงตำแหน่งด้วยตำแหน่ง X, Y เป็นตัวอย่าง
        current_position = (ep_robot.chassis.get_position_x(), ep_robot.chassis.get_position_y())
        path.append(current_position)
        
        time.sleep(0.1)
        
        # ตรวจสอบเวลาที่ผ่านไปในแต่ละรอบ
        if time.time() - round_start_time >= 150:  # 5 นาที = 300 วินาที แบ่งเป็น 2 รอบ 150 วินาที
            rounds += 1
            print(f"จบรอบที่ {rounds}")
            draw_path(path, rounds)
            path.clear()
            round_start_time = time.time()
            
            if rounds >= 2:
                break

def draw_path(path, round_number):
    x = [pos[0] for pos in path]
    y = [pos[1] for pos in path]
    plt.plot(x, y)
    plt.title(f"เส้นทางการเดินในรอบที่ {round_number}")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.savefig(f"path_round_{round_number}.png")
    plt.close()

try:
    move_robot()
except KeyboardInterrupt:
    ep_robot.close()
    print("หยุดการทำงานของหุ่นยนต์")
