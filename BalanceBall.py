from gpiozero import DistanceSensor
from time import sleep
from mpu6050 import mpu6050
import pigpio

sensor_gyro = mpu6050(0x68)
sensor = DistanceSensor(trigger = 20, echo = 21, max_distance=2.0)

servo_pin = 18

pi = pigpio.pi()
pi.set_mode(servo_pin, pigpio.OUTPUT)
pwm_freq = 50   #SC90のPWMサイクル数
time_m90 = 0.5  #-90°のときのパルス時間
time_p90 = 2.4  #+90°のときのパルス時間

pwm_period = 1000 / pwm_freq  #PWM周期時間(msec)
dutyM_m90 = 1e+6 * time_m90 / pwm_period  #-90°のときのduty比(100%は1,000,000)
dutyM_p90 = 1e+6 * time_p90 / pwm_period  #-90°のときのduty比(100%は1,000,000)

def angle_dutyM(deg):
    #角度(°)から、duty比(100%は1,000,000)に換算
    dutyM = int(dutyM_m90 + (dutyM_p90 - dutyM_m90) * ((deg + 90) / 180))
    return dutyM


def servo_test90():
    for i in range(0, -90, -1):
        pi.hardware_PWM(servo_pin, pwm_freq, angle_dutyM(i))
        sleep(0.01)
        #print(i)
    sleep(0.1)

    for i in range(-90, 90):
        pi.hardware_PWM(servo_pin, pwm_freq, angle_dutyM(i))
        sleep(0.01)
        #print(i)
    sleep(0.1)

    for i in range(90, 0, -1):
        pi.hardware_PWM(servo_pin, pwm_freq, angle_dutyM(i))
        sleep(0.01)
        #print(i)
    sleep(0.1)

    pi.hardware_PWM(servo_pin, pwm_freq, 0)
    pi.stop()


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
    servo_test90()
    

if __name__ == '__main__':
    main()