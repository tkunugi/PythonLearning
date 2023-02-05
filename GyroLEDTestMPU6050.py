from mpu6050 import mpu6050
from time import sleep
from gpiozero import LED

sensor = mpu6050(0x68)
led_gyroX = LED(5)
led_gyroY = LED(6)
led_gyroZ = LED(13)
led_accelX = LED(12)
led_accelY = LED(16)
led_accelZ = LED(20)

while True:
    gyro_data = sensor.get_gyro_data()
    accel_data = sensor.get_accel_data()
    #temp = sensor.get_temp

    print(' Gyro x:' + '{:04f}'.format(gyro_data['x']) + ' y:' + '{:04f}'.format(gyro_data['y']) + ' z:' + '{:04f}'.format(gyro_data['z']))
    #print(' Gyro x:' + f'{gyro_data['x']:.4f}' + f'{ y: gyro_data['y']:.4f}' + f' z: {gyro_data['z']:4f}')
    print(' Accel x:' + '{:04f}'.format(accel_data['x']) + ' y:' + '{:04f}'.format(accel_data['y']) + ' z:' + '{:04f}'.format(accel_data['z']))
    #print(' Temp', temp, 'degC')
    #print(gyro_data)

    if gyro_data['x'] >= -1.5 and gyro_data['x'] <= 0.0 :
        led_gyroX.off()
    else:
        led_gyroX.on()
    
    if gyro_data['y'] >= -2.0 and gyro_data['y'] <= 2.0 :
        led_gyroY.off()
    else:
        led_gyroY.on()

    if gyro_data['z'] >= -1.5 and gyro_data['z'] <= -1.0 :
        led_gyroZ.off()
    else:
        led_gyroZ.on()

    if accel_data['x'] >= -1.6 and accel_data['x'] <= -1.2 :
        led_accelX.off()
    else:
        led_accelX.on()

    if accel_data['y'] >= -0.2 and accel_data['y'] <= 0.2 :
        led_accelY.off()
    else:
        led_accelY.on()

    if accel_data['z'] >= 9.3 and accel_data['z'] <= 9.7 :
        led_accelZ.off()
    else:
        led_accelZ.on()

    sleep(1)

