### Script to open the basic data stored on the SD card and plot it with matplotlib

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv('EXAMPLE.TXT',header=0,names=['x','y'])

x = data['x'].to_numpy()
y = data['y'].to_numpy()

fig = plt.figure()

plt.scatter(x,y)
plt.xlabel('x (time in s)')
plt.ylabel('y (random value)')

plt.show()