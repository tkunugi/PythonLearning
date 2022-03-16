from mpu6050 import mpu6050
from time import sleep
import csv
import datetime

sensor = mpu6050(0x68)

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

        sleep(1)
except KeyboardInterrupt:
    f.closed
    raise

