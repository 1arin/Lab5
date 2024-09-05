import time
from robomaster import robot
from robomaster import camera

def measure_camera_and_connection_latency(conn_type):
    # Initialize the robot
    ep_robot = robot.Robot()
    ep_robot.initialize(conn_type=conn_type)
    
    # Start camera stream
    ep_camera = ep_robot.camera
    ep_camera.start_video_stream(display=False)
    
    # Start measuring connection time
    start_time = time.time()
    time.sleep(1)  # Simulate connection time
    end_time = time.time()

    # Calculate latency
    connection_latency = end_time - start_time

    # Stop camera stream
    ep_camera.stop_video_stream()

    # Close connection
    ep_robot.close()

    return connection_latency

if __name__ == "__main__":
    # Measure latency for USB connection with camera
    usb_latency = measure_camera_and_connection_latency('rndis')
    print(f'USB - Connection Latency with Camera: {usb_latency} seconds')
