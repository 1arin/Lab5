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
from robomaster import robot
import csv
import pandas as pd

def sub_position_handler(position_info):
    x, y, z = position_info
    output_list = []
    output_list.append("Chassis position: x:{0}, y:{1}, z:{2}".format(x, y, z))

    # Create a DataFrame from the list
    df = pd.DataFrame(output_list, columns=['Chassis Position'])
    # Display or use the DataFrame
    print(df)

x_val = 0.5
y_val = 0.6
z_val = 90

if __name__ == '__main__':
    ep_robot = robot.Robot()
    ep_robot.initialize(conn_type="ap")

    ep_chassis = ep_robot.chassis

    # 订阅底盘位置信息
    ep_chassis.sub_position(freq=1, callback=sub_position_handler)
    #ep_chassis.move(x=1.0, y=1.0, z=0).wait_for_completed()
    
    ep_chassis.move(x=x_val, y=0, z=0, xy_speed=0.7).wait_for_completed()
     # 左转 90度
    
    # 左移 0.6米
    ep_chassis.move(x=0, y=-y_val, z=0, xy_speed=0.7).wait_for_completed()
    
     # 左转 90度
    
    # 后退 0.5米
    ep_chassis.move(x=-x_val, y=0, z=0, xy_speed=0.7).wait_for_completed()
   
     # 左转 90度
    
    # 右移 0.6米
    ep_chassis.move(x=0, y=y_val, z=0, xy_speed=0.7).wait_for_completed()

   

    # 右转 90度
    #ep_chassis.move(x=0, y=0, z=-z_val, z_speed=45).wait_for_completed()

    ep_chassis.unsub_position()

    ep_robot.close()
