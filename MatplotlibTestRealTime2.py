import numpy as np
import matplotlib.pyplot as plt
import random

fig, ax = plt.subplots(1, 1)
ax.set_ylim((-1.1,1.1))
x = np.arange(-100, 0, 1)
y1 = x * 0.0
y2 = x * 0.0
y1_latest = 0.0
y2_latest = 0.1

while True:
    y1_latest += (random.random() - 0.5) / 10.0
    if y1_latest  > 1 :
        y1_latest = 1
    if y1_latest < -1 :
        y1_latest = -1
    y1 = np.append(y1,y1_latest)
    y1 = np.delete(y1, 0)
    y2_latest += (random.random() - 0.5) / 10.0
    if y2_latest  > 1 :
        y2_latest = 1
    if y2_latest < -1 :
        y2_latest = -1
    y2 = np.append(y2,y2_latest)
    y2 = np.delete(y2, 0)
    line1, = ax.plot(x,y1,color = 'blue')
    line2, = ax.plot(x,y2,color = 'red')
    plt.pause(1)
    line1.remove()
    line2.remove()