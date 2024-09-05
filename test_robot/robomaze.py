import robomaster
from robomaster import robot
import time

class MazeSolver:
    def __init__(self):
        self.tof_distance = None
        self.adc = None
        self.adc_cm = None
        self.status_tof = False
        self.status_ss_1 = False
        
        self.MAX_SPEED = 0.5
        self.WALL_DISTANCE_THRESHOLD = 15
        self.FRONT_DISTANCE_THRESHOLD = 30
        
        self.ep_robot = robot.Robot()
        self.ep_robot.initialize(conn_type="ap")
        self.ep_sensor = self.ep_robot.sensor
        self.ep_chassis = self.ep_robot.chassis
        self.ep_gimbal = self.ep_robot.gimbal
        self.ep_sensor_adaptor = self.ep_robot.sensor_adaptor
        
        self.ep_sensor.sub_distance(freq=10, callback=self.tof_data_handler)
        self.ep_gimbal.recenter().wait_for_completed()

    def tof_data_handler(self, sub_info):
        self.tof_distance = sub_info[0]
        self.status_tof = 50 < self.tof_distance < 300
        
        self.adc = self.ep_sensor_adaptor.get_adc(id=1, port=2)
        self.adc_cm = self.adc_to_cm(self.adc)
        self.status_ss_1 = self.FRONT_DISTANCE_THRESHOLD > self.adc_cm > 5
        
        print(f"Front distance: {self.adc_cm:.2f} cm, ToF distance: {self.tof_distance:.2f} cm")
        print(f"status_tof: {self.status_tof}, status_ss_1: {self.status_ss_1}")

    def adc_to_cm(self, adc):
        adc_to_cm = (adc * 3) / 1023
        if adc_to_cm > 1.4:
            return (adc_to_cm - 4.2) / -0.31
        elif 1.4 >= adc_to_cm >= 0.6:
            return (adc_to_cm - 2.03) / -0.07
        else:
            return (adc_to_cm - 0.95) / -0.016

    def adjust_to_wall(self):
        error = self.WALL_DISTANCE_THRESHOLD - self.adc_cm
        kp = 0.01
        adjustment = kp * error
        return max(min(adjustment, self.MAX_SPEED), -self.MAX_SPEED)

    def check_left(self):
        self.ep_gimbal.move(yaw=90).wait_for_completed()
        time.sleep(0.5)
        left_distance = self.tof_distance
        self.ep_gimbal.recenter().wait_for_completed()
        return left_distance

    def turn_left(self):
        print("Turning left at intersection")
        self.ep_chassis.move(x=0, y=0, z=90, xy_speed=self.MAX_SPEED).wait_for_completed()

    def turn_right(self):
        print("Turning right at wall")
        self.ep_chassis.move(x=0, y=0, z=-90, xy_speed=self.MAX_SPEED).wait_for_completed()
        self.ep_gimbal.recenter().wait_for_completed()

    def move_forward_slowly(self, y_speed):
        self.ep_chassis.move(x=0.1, y=y_speed, z=0, xy_speed=self.MAX_SPEED/2).wait_for_completed()

    def move_forward(self, y_speed):
        self.ep_chassis.drive_speed(x=self.MAX_SPEED, y=y_speed, z=0)

    def stop(self):
        self.ep_chassis.drive_speed(x=0, y=0, z=0)

    def solve_maze(self):
        try:
            while True:
                if self.tof_distance is None or self.adc is None:
                    print("Waiting for sensor data...")
                    time.sleep(0.1)
                    continue

                y_speed = self.adjust_to_wall()

                if self.status_ss_1 and self.status_tof:
                    left_distance = self.check_left()
                    if left_distance > self.WALL_DISTANCE_THRESHOLD:
                        self.turn_left()
                    else:
                        self.turn_right()
                elif self.status_ss_1 and not self.status_tof:
                    self.move_forward_slowly(y_speed)
                elif not self.status_ss_1 and (self.status_tof or self.adc_cm > 30):
                    self.move_forward(y_speed)
                else:
                    self.stop()
                    time.sleep(0.05)

        except KeyboardInterrupt:
            print("Program stopped by user")
        finally:
            self.stop()
            self.ep_sensor.unsub_distance()
            self.ep_robot.close()

if __name__ == "__main__":
    maze_solver = MazeSolver()
    maze_solver.solve_maze()