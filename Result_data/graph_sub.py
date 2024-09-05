import pandas as pd
import matplotlib.pyplot as plt

# sub_ad = pd.read_csv('.\Result_data\sub_attitude_addtime_s1.csv')
# plt.figure(figsize=(10, 5))

# # plt.subplot(2,3,1)
 
# plt.plot(range(1,23),sub_ad["Yaw"], label="Yaw")
# plt.plot(range(1,23),sub_ad["Pitch"], label="Pitch")
# plt.plot(range(1,23),sub_ad["Roll"], label="Roll")
# # plt.xlabel('Time')
# # plt.ylabel('Value')
# plt.title('Attitude Data')
# plt.legend()
# plt.show()

# ----------------------------------------------------------
# sub_esc = pd.read_csv('.\Result_data\sub_esc_s1.csv')

# # plt.subplot(2,3,2)
 
# plt.plot(range(1,22),sub_esc["Speed"], label="Speed")
# plt.plot(range(1,22),sub_esc["Angel"], label="Angle")
# plt.plot(range(1,22),sub_esc["Timestamp"], label="Timestamp")
# plt.plot(range(1,22),sub_esc["State"], label="State")
# # plt.xlabel('Time')
# # plt.ylabel('Value')
# plt.title('Sub ESC')
# plt.grid(True)
# plt.legend()
# plt.show()
# # ----------------------------------------------------------

# sub_imu = pd.read_csv('.\Result_data\sub_imu_s1.csv')

# # plt.subplot(2,3,3)
 
# plt.plot(range(1,22),sub_imu["Acc_X"], label="acc X")
# plt.plot(range(1,22),sub_imu["Acc_Y"], label="acc Y")
# plt.plot(range(1,22),sub_imu["Acc_Z"], label="acc Z")
# # plt.plot(range(1,22),sub_imu["Gyro_X"], label="Gyro X")
# # plt.plot(range(1,22),sub_imu["Gyro_Y"], label="Gyro Y")
# # plt.plot(range(1,22),sub_imu["Gyro_Z"], label="Gyro Z")
# # plt.xlabel('Time')
# # plt.ylabel('Value')
# plt.title('IMU Data X')
# # plt.grid(True)
# plt.legend()
# plt.show()

# # ----------------------------------------------------------

# sub_position = pd.read_csv('.\Result_data\sub_position_s1.csv')

# # plt.subplot(2,3,4)
 
# plt.plot(range(1,22),sub_position["Position X"], label="X")
# plt.plot(range(1,22),sub_position["Position Y"], label="Y")
# # plt.plot(range(1,22),sub_position["Position Z"], label="Position Z")
# # plt.xlabel('Time')
# # plt.ylabel('Value')
# plt.title('Position Data')
# # plt.grid(True)
# plt.legend()
# plt.show()

# ----------------------------------------------------------

sub_tof = pd.read_csv('.\Result_data\sub_tof_s1.csv')

# plt.subplot(2,3,5)
 
plt.plot(range(1,22),sub_tof["tof0"], label="tof0")
plt.plot(range(1,22),sub_tof["tof1"], label="tof1")
plt.plot(range(1,22),sub_tof["tof2"], label="tof2")
plt.plot(range(1,22),sub_tof["tof3"], label="tof3")
plt.xlabel('Time')
plt.ylabel('Value')
plt.title('TOF Data')
plt.grid(True)
plt.legend()
plt.show()