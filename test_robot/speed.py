import time
from robomaster import robot

if __name__ == '__main__':
    ep_robot = robot.Robot()
    ep_robot.initialize(conn_type="ap")

    ep_chassis = ep_robot.chassis

    x_val = 0.5
    xy_speed = 0.7

    # Record the start time
    start_time = time.time()

    # Move forward 0.5 meters
    ep_chassis.drive_speed(x=x_val, y=0, z=0, timeout=1).wait_for_completed()

    # Record the end time
    end_time = time.time()

    # Calculate the time taken
    time_taken = end_time - start_time

    # Calculate the actual speed
    actual_speed = x_val / time_taken

    # Print the actual speed
    print(f"The actual speed of the robot is {actual_speed:.2f} m/s")
