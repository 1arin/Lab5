import asyncio
import cv2
import time
from robomaster import robot
from robomaster import vision

class PointInfo:
    def __init__(self, x, y, theta, c):
        self._x = x
        self._y = y
        self._theta = theta
        self._c = c

    @property
    def pt(self):
        return int(self._x * 1280), int(self._y * 720)

    @property
    def color(self):
        return 255, 255, 255

line = []

def on_detect_line(line_info):
    number = len(line_info)
    line.clear()
    line_type = line_info[0]
    print('line_type', line_type)
    for i in range(1, number):
        x, y, ceta, c = line_info[i]
        line.append(PointInfo(x, y, ceta, c))

async def capture_and_save_image(ep_camera, filename):
    img = ep_camera.read_cv2_image(strategy="newest")
    cv2.imwrite(filename, img)
    print(f"Image saved as {filename}")

async def main():
    # Initialize the robot
    ep_robot = robot.Robot()
    ep_robot.initialize(conn_type="rndis")  # หรือใช้ "rndis" ตามการเชื่อมต่อของคุณ

    ep_vision = ep_robot.vision
    ep_camera = ep_robot.camera

    # Start camera stream with STREAM_720P
    ep_camera.start_video_stream(display=False, resolution="720p")

    # Subscribe to line detection
    result = ep_vision.sub_detect_info(name="line", color="blue", callback=on_detect_line)

    try:
        # Capture and display images for 10 seconds
        start_time = asyncio.get_event_loop().time()
        frame_count = 0
        while asyncio.get_event_loop().time() - start_time < 10:
            img = ep_camera.read_cv2_image(strategy="newest")
            
            # Draw detected lines
            for point in line:
                cv2.circle(img, point.pt, 3, point.color, -1)
            
            cv2.imshow("Robot Camera", img)
            key = cv2.waitKey(1) & 0xFF
            
            # Capture image when 'c' is pressed
            if key == ord('c'):
                await capture_and_save_image(ep_camera, f"captured_image_{frame_count}.jpg")
                frame_count += 1
            
            # Exit loop if 'q' is pressed
            elif key == ord('q'):
                break
            
            await asyncio.sleep(0.03)  # Approx. 30 FPS

    finally:
        # Clean up
        cv2.destroyAllWindows()
        ep_vision.unsub_detect_info(name="line")
        ep_camera.stop_video_stream()
        ep_robot.close()

if __name__ == "__main__":
    asyncio.run(main())