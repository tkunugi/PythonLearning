#from turtle import distance
from gpiozero import AngularServo, DistanceSensor
from time import sleep
from mpu6050 import mpu6050


servo = AngularServo(5, min_pulse_width=0.5/1000, max_pulse_width=2.4/1000)
sensor_gyro = mpu6050(0x68)
sensor = DistanceSensor(trigger = 20, echo = 21, max_distance=2.0)

def servo_test():
    #サーボモーターの駆動チェック　回転位置が0°→-5°→+5°→0°で駆動
    for i in list(range(0,-5,-1)):
        servo.angle = i
        sleep(0.5)
    
    for i in list(range(-5,5, 1)):
        servo.angle = i
        sleep(0.5)

    for i in list(range(5,0,-1)):
        servo.angle = i
        sleep(0.5)

    servo.angle = 0

def servo_test90():
    #サーボモーターの駆動チェック　回転位置が0°→-90°→+90°→0°で駆動
    for i in list(range(0,-90,-1)):
        servo.angle = i
        sleep(0.1)
    
    for i in list(range(-90,90, 1)):
        servo.angle = i
        sleep(0.1)

    for i in list(range(90,0,-1)):
        servo.angle = i
        sleep(0.1)

    servo.angle = 0

def gyro_test():
    #ジャイロセンサーのテスト　読み取り値を1秒ごとに3回表示
    for i in range(3):
        gyro_data = sensor_gyro.get_gyro_data()
        accel_data = sensor_gyro.get_accel_data()

        print(' Gyro x:' + '{:04f}'.format(gyro_data['x']) + ' y:' + '{:04f}'.format(gyro_data['y']) + ' z:' + '{:04f}'.format(gyro_data['z']))
        print(' Accel x:' + '{:04f}'.format(accel_data['x']) + ' y:' + '{:04f}'.format(accel_data['y']) + ' z:' + '{:04f}'.format(accel_data['z']))
    
        sleep(1)

def dist_test():
    #距離センサーのテスト　読み取り値を1秒ごとに3回表示
    for i in range(3):
        distance = sensor.distance * 100
        print('Distance : %.1f' % distance)
        sleep(1)


def main():
    #servo_test()
    #gyro_test()
    #dist_test()
    #servo.test90()
    servo.angle = 0

if __name__ == '__main__':
    main()