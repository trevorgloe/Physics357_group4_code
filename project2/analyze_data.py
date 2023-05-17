### Script to read and analyze gyroscope and accelerometer data read from the SD card, produced by the arduino
# Written for project 2, Physics 357 Spring 2023 with Dr. Fernsler
# Data is stored in csv file called DATA.TXT - contains accelerometer data in 2 dimensions (x and y) and angular rates in z
# 
# 

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# read data from csv
data = pd.read_csv('Data/run_01.TXT')
print(data)

# extract data into numpy arrays
tstr = data['time'].to_numpy()
axstr = data['AcX'].to_numpy()
aystr = data['AcY'].to_numpy()
gzstr = data['GyZ'].to_numpy()

# truncate the data to avoid weird stuff and cast as floats
t = tstr[2:].astype(float)
ax = axstr[2:].astype(float)
ay = aystr[2:].astype(float)
gz = gzstr[2:].astype(float)
print(ax)

# integrate the gryo data just for fun
int_ang = np.zeros(gz.shape)
for idx in range(len(t)):
    int_ang[idx] = np.trapz(gz[:idx],t[:idx])


fig_accel = plt.figure()

plt.scatter(t,ax,color='r',label='x-axis',s=2)
plt.scatter(t,ay,color='b',label='y-axis',s=2)
plt.xlabel('Time (ms)')
plt.ylabel('Acceleration')
plt.legend()
#plt.xticks(np.arange(np.min(t),np.max(t),5000))

fig_gyr = plt.figure()
plt.scatter(t,gz,color='r',s=2)
plt.xlabel('Time (ms)')
plt.ylabel('Angular rate')

fig_ang = plt.figure()
plt.scatter(t,int_ang,color='b',s=2)
plt.xlabel('Time (ms)')
plt.ylabel('Angle integrated from gyro data')

plt.show()