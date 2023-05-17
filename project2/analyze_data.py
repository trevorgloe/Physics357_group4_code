### Script to read and analyze gyroscope and accelerometer data read from the SD card, produced by the arduino
# Written for project 2, Physics 357 Spring 2023 with Dr. Fernsler
# Data is stored in csv file called DATA.TXT - contains accelerometer data in 2 dimensions (x and y) and angular rates in z
# 
# 
# The radius from the center of chair to the gyroscope is 15.5 cm
# The accelerometer x direction points in the phi_hat direction, and y points radially outward
#
# the gyroscope sensativity is set at 250 deg/s total
# so the actual rate in terms of the gryo value is rate = 250/32750 * gryo_val
#
# the accelerometer sensativity is set at 2g total
# so the actual acceleration read in terms of the gryo is 2*9.81/32750 * accel_val



import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


## functions for mapping the read values into real numbers
def map_gryo(val):
    degsec =  250/32750 * val
    return degsec*np.pi/180

def map_accel(val):
    return 2*9.81/32750 * val


# read data from csv
data = pd.read_csv('Data/run_15.TXT')
print(data)

# extract data into numpy arrays
tstr = data['time'].to_numpy()
axstr = data['AcX'].to_numpy()
aystr = data['AcY'].to_numpy()
gzstr = data['GyZ'].to_numpy()

# truncate the data to avoid weird stuff and cast as floats
trunkval=1600
tread = tstr[trunkval:].astype(float)
axread = axstr[trunkval:].astype(float)
ayread = aystr[trunkval:].astype(float)
gzread = gzstr[trunkval:].astype(float)

# convert the values to physical numbers
t = (tread - tread[0])/1e3
ax = map_accel(axread)
ay = map_accel(ayread)
gz = map_gryo(gzread)

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

## compute derivative of gyroscope data
deriv_gryo = np.gradient(gz,t)

fig_deriv = plt.figure()
plt.scatter(t,np.abs(deriv_gryo),color='g',s=2)
plt.xlabel('Time (ms)')
plt.ylabel('Differentiated Gryscope (Angular Acceleration)')

## plot acceleration vs. rate
force_comp1_fig = plt.figure()
plt.scatter(gz,np.abs(deriv_gryo),color='r',s=2)
plt.xlabel('Angular rate')
plt.ylabel('Angular acceleration')

plt.show()