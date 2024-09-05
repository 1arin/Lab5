# -*-coding:utf-8-*-
# Copyright (c) 2020 DJI.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License in the file LICENSE.txt or at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import robomaster
import time
from robomaster import robot

# ฟังก์ชันสำหรับการเดินไปข้างหน้า
def move_forward(ep_chassis, distance, speed):
    step_length = 0.1  # ระยะทางต่อการเดินหนึ่งครั้งในหน่วยซม
    num_steps = int(distance / step_length)
    
    for _ in range(num_steps):
        ep_chassis.drive_wheels(w1=speed, w2=speed, w3=speed, w4=speed)
        time.sleep(0.1)  # หน่วงเวลา 0.1 วินาทีต่อการเดินแต่ละครั้ง
    ep_chassis.drive_wheels(w1=0, w2=0, w3=0, w4=0)
    time.sleep(0.1)  # หน่วงเวลาให้หยุดสนิทก่อนเริ่มเดินใหม่

if __name__ == '__main__':
    ep_robot = robot.Robot()
    ep_robot.initialize(conn_type="sta")

    ep_chassis = ep_robot.chassis
    speed = 30  # ปรับค่าความเร็วตามความเหมาะสม
    side_length = 60  # ความยาวด้านของสี่เหลี่ยมจัตุรัสในหน่วยซม

    # เดินไปข้างหน้า
    move_forward(ep_chassis, side_length, speed)

    # เคลื่อนที่ทางขวา
    ep_chassis.drive_wheels(w1=-speed, w2=speed, w3=-speed, w4=speed)
    time.sleep(2.0)  # ปรับเวลาให้เหมาะสมสำหรับการเคลื่อนที่ 60 ซม
    ep_chassis.drive_wheels(w1=0, w2=0, w3=0, w4=0)
    time.sleep(0.1)  # หน่วงเวลาให้หยุดสนิทก่อนเริ่มเดินใหม่

    # เดินถอยหลัง
    move_forward(ep_chassis, side_length, -speed)

    # เคลื่อนที่ทางซ้าย
    ep_chassis.drive_wheels(w1=speed, w2=-speed, w3=speed, w4=-speed)
    time.sleep(2.0)  # ปรับเวลาให้เหมาะสมสำหรับการเคลื่อนที่ 60 ซม
    ep_chassis.drive_wheels(w1=0, w2=0, w3=0, w4=0)
    time.sleep(0.1)  # หน่วงเวลาให้หยุดสนิทก่อนเริ่มเดินใหม่

    ep_robot.close()
