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
from scipy.optimize import curve_fit


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

# function for fitting
def power_law(x,a,b):
    # a is the scale factor out front, b is the power

    return a*pow(x,b)

for j,file in enumerate(datafiles):

    print(j)
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
    trunkval=trunk[j]

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
        ax = -ax

    # print(ax)

    # integrate the gryo data just for fun
    int_ang = np.zeros(gz.shape)
    for idx in range(len(t)):
        int_ang[idx] = np.trapz(gz[:idx],t[:idx])


    # compute centripital acceleration
    a_c = r*gz**2  # r * omega^2

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


    # plot the gz
    plt.figure()
    plt.scatter(t,gz,color='b',s=2)

    # get rid of nans in the data
    print(len(np.isnan(gz)))
    print(len(a_angx))
    a_angx = a_angx[~np.isnan(gz)]
    gz = gz[~np.isnan(gz)]
    # print(gz)
    # print(a_angx)

    # get rid of initial small omegas
    a_angx = a_angx[gz>0.08]
    gz = gz[gz>0.08]

    # fit the curve
    popt, pcov = curve_fit(power_law,gz,a_angx)

    print(popt)
    # plot the accerlation in x vs. 
    # x acceleration is in the phi-hat direction
    plt.figure()
    plt.scatter(gz,a_angx,color='b',s=2,label='data')
    plt.scatter(np.linspace(np.nanmin(gz),np.nanmax(gz)),power_law(np.linspace(np.nanmin(gz),np.nanmax(gz)),popt[0],popt[1]),label='fit')
    plt.xlabel('$\omega$ [rad/s]')
    plt.ylabel(r'$\alpha$ [rad/s^2]')

    all_scales[j] = popt[0]
    all_powers[j] = popt[1]



plt.figure()
plt.scatter(np.arange(0,len(all_powers)),all_powers,color='r')
good_pow = np.copy(all_powers)
good_pow[2] = 'nan'
good_pow[12] = 'nan'
good_pow[13] = 'nan'
plt.scatter(np.arange(0,len(all_powers)),good_pow,color='b')
plt.ylabel('fitted powers')
avg_pow = np.nanmean(good_pow)
print('Average exponent: '+str(avg_pow))
plt.plot([0,len(all_powers)],[avg_pow,avg_pow],color='g')


plt.figure()
plt.scatter(np.arange(0,len(all_scales)),all_scales,color='r')
plt.ylabel('fitted scale factors')
good_scale = np.copy(all_scales)
good_scale[6] = 'nan'
good_scale[8] = 'nan'
good_scale[14] = 'nan'
plt.scatter(np.arange(0,len(all_scales)),good_scale,color='b')
# plt.ylabel('fitted powers')
avg_scale = np.nanmean(good_scale)
print('Average scale-factor: '+str(avg_scale))
plt.plot([0,len(all_scales)],[avg_scale,avg_scale],color='g')

plt.show()



