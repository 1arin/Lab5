import robomaster
import time
import math
from robomaster import robot
import matplotlib.pyplot as plt
import pandas as pd

# Initialize position library
position_lib = []

def sub_position_handler(position_info):
    x, y, z = position_info
    print("chassis position: x:{0}, y:{1}, z:{2}".format(x, y, z))
    position_lib.append((x, y, z))

if __name__ == '__main__':
    ep_robot = robot.Robot()
    ep_robot.initialize(conn_type="ap")

    ep_chassis = ep_robot.chassis

    # Calculate speed and parameters
    distance_cm = 120
    diameter = (5 * (2 * math.pi)) / 60
    slp = 5
    speed = distance_cm / (diameter * slp)

    # PID controller constant
    p = 12

    # Subscribe to position updates
    ep_chassis.sub_position(freq=10, callback=sub_position_handler)

    ep_chassis.drive_wheels(w1=0, w2=0, w3=0, w4=0)
    time.sleep(slp)
    
    # Move forward 120 cm
    ep_chassis.drive_wheels(w1=speed, w2=speed, w3=speed, w4=speed)
    time.sleep(slp)

    ep_chassis.drive_wheels(w1=0, w2=0, w3=0, w4=0)
    time.sleep(slp)

    # Move backward 120 cm
    ep_chassis.drive_wheels(w1=-speed, w2=-speed, w3=-speed, w4=-speed)
    time.sleep(slp)
    
    ep_chassis.drive_wheels(w1=0, w2=0, w3=0, w4=0)
    time.sleep(slp)
    
    # Move forward 120 cm
    ep_chassis.drive_wheels(w1=speed, w2=speed, w3=speed, w4=speed)
    time.sleep(slp)

    ep_chassis.drive_wheels(w1=0, w2=0, w3=0, w4=0)
    time.sleep(slp)

    # Move backward 120 cm
    ep_chassis.drive_wheels(w1=-speed, w2=-speed, w3=-speed, w4=-speed)
    time.sleep(slp)

    ep_chassis.drive_wheels(w1=0, w2=0, w3=0, w4=0)
    time.sleep(slp)
    
    # Move forward 120 cm
    ep_chassis.drive_wheels(w1=speed, w2=speed, w3=speed, w4=speed)
    time.sleep(slp)

    ep_chassis.drive_wheels(w1=0, w2=0, w3=0, w4=0)
    time.sleep(slp)

    # Move backward 120 cm
    ep_chassis.drive_wheels(w1=-speed, w2=-speed, w3=-speed, w4=-speed)
    time.sleep(slp)

    # Stop
    # ep_chassis.drive_speed(x=0, y=0, z=0, timeout=4.5)
    # time.sleep(slp)

    # Calculate errors
    # err_x = distance_cm - (position_lib[-1][0] * 100)
    # err_y = 0 - (position_lib[-1][1] * 100)

    # print(f"Initial errors: err_x: {err_x}, err_y: {err_y}")

    # err_ok = 1
    # while abs(err_x) > err_ok or abs(err_y) > err_ok:
    #     speed_feedback = 0.5 * p

    #     # Apply corrections
    #     ep_chassis.drive_wheels(w1=speed_feedback, w2=speed_feedback, w3=speed_feedback, w4=speed_feedback)
    #     time.sleep(slp)
    #     ep_chassis.drive_wheels(w1=-speed_feedback, w2=-speed_feedback, w3=-speed_feedback, w4=-speed_feedback)
    #     time.sleep(slp)
    #     ep_chassis.drive_speed(x=0, y=0, z=0, timeout=4.5)
    #     time.sleep(slp)

    #     err_x = distance_cm - (position_lib[-1][0] * 100)
    #     err_y = 0 - (position_lib[-1][1] * 100)
    #     print(f"Updated errors: err_x: {err_x}, err_y: {err_y}")
    #     ep_chassis.unsub_position()

    # Final stop
    # ep_chassis.drive_speed(x=0, y=0, z=0, timeout=4.5)
    # time.sleep(slp)

    # print(f"Final position: x: {position_lib[-1][0]}, y: {position_lib[-1][1]}")

    # Unsubscribe from position updates
    ep_chassis.drive_wheels(w1=speed, w2=speed, w3=speed, w4=speed)
    time.sleep(slp)

    # Move backward 120 cm
    ep_chassis.drive_wheels(w1=-speed, w2=-speed, w3=-speed, w4=-speed)
    time.sleep(slp)
    
    ep_chassis.unsub_position()

    # Close the robot connection
    ep_robot.close()

    # Plot the position data
    plt.figure(figsize=(10, 5))
    plt.plot([pos[0] for pos in position_lib], [pos[1] for pos in position_lib], marker='o')
    plt.title("Robot Chassis Position")
    plt.xlabel("Time (s)")
    plt.ylabel("Position (m)")
    plt.show()
