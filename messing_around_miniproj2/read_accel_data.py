### Script to open the basic data stored on the SD card and plot it with matplotlib

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv('EXAMPLE.TXT')
print(data)

tstr = data['time'].to_numpy()
axstr = data['AcX'].to_numpy()
aystr = data['AcY'].to_numpy()

# truncate the data to avoid weird stuff
t = tstr[3:].astype(float)
ax = axstr[3:].astype(float)
ay = aystr[3:].astype(float)
print(ax)

fig = plt.figure()

plt.scatter(t,ax,color='r',label='x-axis')
plt.scatter(t,ay,color='b',label='y-axis')
plt.xlabel('Time (ms)')
plt.ylabel('Acceleration')
plt.legend()
plt.xticks(np.arange(np.min(t),np.max(t),5000))

plt.show()