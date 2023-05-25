### script to find the moment of inertia of the chair using a linear fit

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
from scipy.optimize import curve_fit

# functions for mapping the read values into real numbers
def map_gryo(val):
    degsec =  250/32750 * val
    return degsec*np.pi/180

def map_accel(val):
    return 2*9.81/32750 * val


## make a list of all data files
datadir = 'Data/I_measure'
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
# all_scales = np.zeros(N)
# all_powers = np.zeros(N)
r = 0.155 # in m

# make array of added moments of interia
m1 = 1.435  # kg
m2 = 1.0    # kg
r1 = 0.025  # m
r2 = 0.024  # m   

r = 0.155 # location of acceleratometer in m

I = np.zeros(10)
I[0] = 0        # no added weight
I[1] = 1/2*m1*r1**2
I[2] = 1/2*m1*r1**2 + m2*0.16**2
I[3] = 1/2*m1*r1**2 + m2*0.1**2
I[4] = 1/2*m1*r1**2 + m2*0.185**2
I[5] = m1*0.16**2
I[6] = m1*0.1**2
I[7] = m1*0.19**2
I[8] = m1*0.19**2 + m2*0.2**2
I[9] = m1*0.1**2 + m2*0.16**2

# truncation values
trunk = [1,1,1,1,1,1,1,1,1061,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

# array of numbers saying which run of each setup we take
whichrun = np.array([0,0,1,0,1,0,1,1,1,1])

good_names = []
strruns = whichrun + 1
for i in range(len(whichrun)):
    good_names.append('s'+str(i)+'_r'+str(strruns[i])+'.TXT')

print(good_names)


## allocate arrays for final data we want to collect
all_alpha = np.zeros(len(good_names))
w = 1.9    # the omega value at which we want to look at the acceleration

# function for fitting
def linear(x,a,b):
    # a is the scale factor out front, b is the power

    return a*x+b

for j,file in enumerate(datafiles):

    print(j)
    print(file)

    # get the data
    # read data from csv
    data = pd.read_csv(os.path.join('Data/I_measure',file))
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

    plt.figure()
    plt.scatter(t,ax,color='b',s=2)
    plt.title(file)
    plt.scatter(t,gz,color='g',s=2)

for j,file in enumerate(good_names):
    print(j)
    print(file)

    # get the data
    # read data from csv
    data = pd.read_csv(os.path.join('Data/I_measure',file))
    # print(data)

    # extract data into numpy arrays
    tstr = data['time'].to_numpy()
    axstr = data['AcX'].to_numpy()
    aystr = data['AcY'].to_numpy()
    gzstr = data['GyZ'].to_numpy()

    # truncate the data to avoid weird stuff and cast as floats
    trunkval=trunk[j]

    ## find point of maximum omega

    tread = tstr[1:].astype(float)
    axread = axstr[1:].astype(float)
    ayread = aystr[1:].astype(float)
    gzread = gzstr[1:].astype(float)

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


    # get acceleration at specified omega
    ptarray = np.where(np.abs(gz-w)==np.nanmin(np.abs(gz-w)))
    pt = ptarray[0][0]

    accel = ax[pt]/r

    all_alpha[j] = accel


## plot I vs 1/alpha
overalpha = np.power(all_alpha,-1)
print(overalpha)
print(I)

# get rid of second data point 
temp_oalpha = np.copy(overalpha)
temp_oalpha[1] = 'nan'
temp_oalpha[0] = 'nan'
overalpha = temp_oalpha[~np.isnan(temp_oalpha)]
I = I[~np.isnan(temp_oalpha)]


plt.figure()
plt.scatter(overalpha,I,color='b',label='Data points')
popt, pcov = curve_fit(linear,overalpha,I)
plt.scatter(np.linspace(np.min(overalpha),np.max(overalpha),500),linear(np.linspace(np.min(overalpha),np.max(overalpha),500),popt[0],popt[1]),color='r',s=2,label='Fitted Line')
plt.xlabel(r'$1/\alpha\frac{s^2}{rad}$')
plt.ylabel('$I_{added}$ [kg$m^2$]')
print('Fitted tau: '+str(popt[0]))
print('Fitted I: '+str(-popt[1]))
plt.legend()
plt.show()