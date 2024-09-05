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

    # Move forward 0.5 meters with a timeout
    ep_chassis.drive_speed(x=0.7, y=0, z=0,timeout = 1)
    time.sleep(2)
    # time.sleep(x_val / xy_speed)  # Wait for the estimated time it takes to move 0.5 meters

    # # Stop the robot
    # ep_chassis.drive_speed(x=0, y=0, z=0)

    # Record the end time
    end_time = time.time()

    # Calculate the time taken
    time_taken = end_time - start_time

    # Calculate the actual speed
    # actual_speed = x_val / time_taken

    # Print the actual speed
    print(f"The actual speed of the robot is {actual_speed:.2f} m/s")
    print(time_taken)

    ep_robot.close()