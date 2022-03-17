from mpu6050 import mpu6050
from time import sleep
import csv
import datetime
import numpy as np
import matplotlib.pyplot as plt

sensor = mpu6050(0x68)

#リアルタイムプロットの設定
fig, ax = plt.subplots(1, 1)
ax.set_ylim((-2.1,1.1))
ax.set_xlabel('time (- sec.)')
#ax.legend(['GyroX', 'GyroY', 'GyroZ', 'AccelX', 'AccelY'])
#ax.legend(loc='upper right')
x = np.arange(-100, 0, 1)
plotArrayGyroX = x * 0.0
plotArrayGyroY = x * 0.0
plotArrayGyroZ = x * 0.0
plotArrayAccelX = x * 0.0
plotArrayAccelY = x * 0.0

now = datetime.datetime.now()
now_f = now.strftime("%Y%m%d%H%M%S")

fname = '../data/gyro'+now_f+'.csv'
f = open(fname, 'w', newline = '')

writer = csv.writer(f)
writer.writerow(['DateTime', 'GyroX', 'GyroY', 'GyroZ', 'AccelX', 'AccelY', 'AccelZ'])

try:
    while True:
        now = datetime.datetime.now()
        now_f = now.strftime("%Y/%m/%d %H:%M:%S")

        gyro_data = sensor.get_gyro_data()
        accel_data = sensor.get_accel_data()

        gyroX = '{:04f}'.format(gyro_data['x'])
        gyroY = '{:04f}'.format(gyro_data['y'])
        gyroZ = '{:04f}'.format(gyro_data['z'])
        accelX = '{:04f}'.format(accel_data['x'])
        accelY = '{:04f}'.format(accel_data['y'])
        accelZ = '{:04f}'.format(accel_data['z'])

        #print(' Gyro x:' + '{:04f}'.format(gyro_data['x']) + ' y:' + '{:04f}'.format(gyro_data['y']) + ' z:' + '{:04f}'.format(gyro_data['z']))
        print(' Gyro x:' + gyroX + ' y:' + gyroY + ' z:' + gyroZ)
        #print(' Accel x:' + '{:04f}'.format(accel_data['x']) + ' y:' + '{:04f}'.format(accel_data['y']) + ' z:' + '{:04f}'.format(accel_data['z']))
        print(' Accel x:' + accelX + ' y:' + accelY + ' z:' + accelZ)

        writer.writerow([now_f, gyroX, gyroY, gyroZ, accelX, accelY, accelZ])

        plotArrayGyroX = np.append(plotArrayGyroX, gyro_data['x'])
        plotArrayGyroX = np.delete(plotArrayGyroX, 0)
        plotArrayGyroY = np.append(plotArrayGyroY, gyro_data['y'])
        plotArrayGyroY = np.delete(plotArrayGyroY, 0)
        plotArrayGyroZ = np.append(plotArrayGyroZ, gyro_data['z'])
        plotArrayGyroZ = np.delete(plotArrayGyroZ, 0)
        plotArrayAccelX = np.append(plotArrayAccelX, accel_data['x'])
        plotArrayAccelX = np.delete(plotArrayAccelX, 0)
        plotArrayAccelY = np.append(plotArrayAccelY, accel_data['y'])
        plotArrayAccelY = np.delete(plotArrayAccelY, 0)
        line1, = ax.plot(x,plotArrayGyroX,color = 'blue', label="GyroX")
        line2, = ax.plot(x,plotArrayGyroY,color = 'green', label='GyroY')
        line3, = ax.plot(x,plotArrayGyroZ,color = 'purple', label='GyroZ')
        line4, = ax.plot(x,plotArrayAccelX,color = 'red', label='AccelX')
        line5, = ax.plot(x,plotArrayAccelY,color = 'orange', label='AccelY')
        ax.legend(loc='upper left')
        plt.pause(1)
        line1.remove()
        line2.remove()
        line3.remove()
        line4.remove()
        line5.remove()

        #sleep(1)
except KeyboardInterrupt:
    f.closed
    raise

