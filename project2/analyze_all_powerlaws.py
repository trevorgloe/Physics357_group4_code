### look at all runs and calculate all power laws between acceleration and velocity
# then take the average of all slopes
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
import os


## functions for mapping the read values into real numbers
def map_gryo(val):
    degsec =  250/32750 * val
    return degsec*np.pi/180

def map_accel(val):
    return 2*9.81/32750 * val


## make a list of all data files
datadir = 'Data'
all_files = os.listdir(datadir)

print(all_files)

datafiles = []
for file in all_files:
    if '.TXT' in file:
        datafiles.append(file)

print(datafiles)

## loop through all data files and do the analysis on each one
# allocate arrays for the power and the scale
N = len(datafiles)
all_scales = np.zeros(N)
all_powers = np.zeros(N)
r = 0.155 # in m

# truncation values for all files
trunk = [975,2,90,2,415,1510,2,1372,318,2,282,884,97,65,2395]

for idx,file in enumerate(datafiles):

    print(idx)
    print(file)

    # get the data
    # read data from csv
    data = pd.read_csv(os.path.join('Data',file))
    # print(data)

    # extract data into numpy arrays
    tstr = data['time'].to_numpy()
    axstr = data['AcX'].to_numpy()
    aystr = data['AcY'].to_numpy()
    gzstr = data['GyZ'].to_numpy()

    # truncate the data to avoid weird stuff and cast as floats
    trunkval=trunk[idx]

    ## find point of maximum omega

    tread = tstr[trunkval:].astype(float)
    axread = axstr[trunkval:].astype(float)
    ayread = aystr[trunkval:].astype(float)
    gzread = gzstr[trunkval:].astype(float)

    # print(np.max(gzread))
    max_om_pt_ar = np.where(np.abs(gzread)==np.nanmax(np.abs(gzread)))
    max_om_pt = max_om_pt_ar[0][0]
    print(max_om_pt)
    # trunkate all arrays by this index
    ttemp = tread[max_om_pt+1:]
    axtemp = axread[max_om_pt+1:]
    aytemp = ayread[max_om_pt+1:]
    gztemp = gzread[max_om_pt+1:]

    # convert the values to physical numbers
    t = (ttemp - ttemp[0])/1e3
    ax = map_accel(axtemp)
    ay = map_accel(aytemp)
    gz = map_gryo(gztemp)

    # if the gyroscope velocity is negative then make it all negative
    if gz[1]<0:
        gz = -gz

    # print(ax)

    # integrate the gryo data just for fun
    int_ang = np.zeros(gz.shape)
    for idx in range(len(t)):
        int_ang[idx] = np.trapz(gz[:idx],t[:idx])


    # compute centripital acceleration
    a_c = r*gz  # r * omega^2

    # the centripital acceleration points in the x direction so subtract it off
    a_angx = (ax)/r
    a_angy = (ay + a_c)/r

    # print(a_angx)
    # print(a_angy)

    # plot the accelrations
    # plt.figure()

    # plt.scatter(t,ax,color='r',label='x',s=2)
    # plt.scatter(t,ay,color='b',label='y',s=2)
    # plt.scatter(t,a_c,color='g',label='centripital',s=2)

    # plt.legend()

    # plot the accerlation in x vs. 
    # x acceleration is in the phi-hat direction
    plt.figure()
    plt.scatter(gz,a_angx,color='b',s=2)
    plt.xlabel('$\omega$ [rad/s]')
    plt.ylabel(r'$\alpha$ [rad/s^2]')

    # plot the gz
    plt.figure()
    plt.scatter(t,gz,color='b',s=2)

    


plt.show()



