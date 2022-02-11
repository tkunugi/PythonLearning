from mpu6050 import mpu6050
from time import sleep

sensor = mpu6050(0x68)

while True:
    gyro_data = sensor.get_gyro_data()
    accel_data = sensor.get_accel_data()
    #temp = sensor.get_temp

    print(' Gyro x:' + '{:04f}'.format(gyro_data['x']) + ' y:' + '{:04f}'.format(gyro_data['y']) + ' z:' + '{:04f}'.format(gyro_data['z']))
    #print(' Gyro x:' + f'{gyro_data['x']:.4f}' + f'{ y: gyro_data['y']:.4f}' + f' z: {gyro_data['z']:4f}')
    print(' Accel x:' + '{:04f}'.format(accel_data['x']) + ' y:' + '{:04f}'.format(accel_data['y']) + ' z:' + '{:04f}'.format(accel_data['z']))
    #print(' Temp', temp, 'degC')
    #print(gyro_data)

    sleep(1)

