import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# อ่านข้อมูลจากไฟล์ .csv
df_ap = pd.read_csv('new_ap_500.csv', header=None, names=['Value'])
df_rndis = pd.read_csv('new_rndis_500.csv', header=None, names=['Value'])

# เพิ่มคอลัมน์ประเภทการเชื่อมต่อ
df_ap['Type'] = 'AP'
df_rndis['Type'] = 'RNDIS'

# รวมข้อมูลจากทั้งสองไฟล์
df = pd.concat([df_ap, df_rndis])

# สร้างตำแหน่งของแท่งกราฟ
positions = np.arange(len(df))

# พล็อตกราฟแท่ง
plt.figure(figsize=(2,6))
plt.bar(positions, df['Value'], color=['blue', 'green'], width=0.7)
plt.xlabel('Connection Type')
plt.ylabel('Value')
plt.title('Comparison of Connection Types')
plt.ylim(0, max(df['Value']) + 1)
plt.xticks(positions, df['Type'])

# แสดงกราฟ
plt.show()
