import numpy as np
from gpiozero import DistanceSensor
from time import sleep
from mpu6050 import mpu6050
import pigpio

sensor_gyro = mpu6050(0x68)
sensor = DistanceSensor(trigger = 20, echo = 21, max_distance=2.0)

servo_pin = 18
duty_arm_calib = 0  #アームの初期角度補正用
duty_m5deg = 0 #duty値変数の設定
duty_p5deg = 0 #duty値変数の設定
duty_0deg = 0 #duty値変数の設定

pi = pigpio.pi()
pi.set_mode(servo_pin, pigpio.OUTPUT)
pwm_freq = 50   #SC90のPWMサイクル数
time_m90 = 0.5  #-90°のときのパルス時間
time_p90 = 2.4  #+90°のときのパルス時間

pwm_period = 1000 / pwm_freq  #PWM周期時間(msec)
dutyM_m90_raw = 1e+6 * time_m90 / pwm_period  #-90°のときのduty比(100%は1,000,000)、角度補正なし
dutyM_p90_raw = 1e+6 * time_p90 / pwm_period  #-90°のときのduty比(100%は1,000,000)、角度補正なし

def angle_dutyM(deg):
    #角度(°)から、duty比(100%は1,000,000)に換算
    dutyM = int(dutyM_m90_raw + (dutyM_p90_raw - dutyM_m90_raw) * ((deg + 90) / 180))
    return dutyM


def servo_test90():
    #サーボモーターの駆動テスト用(アームなしでのテスト用)　-0°→　-90° → +90° → 0°
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

def servo_test0():
    #サーボモーターの駆動テスト用(アームありでのテスト用) -0°→ -5° → +5° → 0°
    for i in np.arange(0., -5., -1):
        pi.hardware_PWM(servo_pin, pwm_freq, angle_dutyM(i))
        sleep(0.1)
        pi.hardware_PWM(servo_pin, pwm_freq, 0)
        sleep(2)
        print(i)
    sleep(0.1)

    for i in np.arange(-5., 5., 1):
        pi.hardware_PWM(servo_pin, pwm_freq, angle_dutyM(i))
        sleep(0.1)
        pi.hardware_PWM(servo_pin, pwm_freq, 0)
        sleep(2)
        print(i)
    sleep(0.1)

    for i in np.arange(5., 0., -1):
        pi.hardware_PWM(servo_pin, pwm_freq, angle_dutyM(i))
        sleep(0.1)
        pi.hardware_PWM(servo_pin, pwm_freq, 0)
        sleep(2)
        print(i)
    sleep(0.1)

    pi.hardware_PWM(servo_pin, pwm_freq, 0)
    pi.stop()

def servo_test():
    #サーボモーターの駆動テスト用(アームありでのテスト用) -0°→ -5° → +5° → 0°
    # 角度変換関数を関数実行直後に使用し、その後直接数値で駆動することにより高速化を図った
    
    for i in range(duty_0deg, duty_m5deg, -10):
        pi.hardware_PWM(servo_pin, pwm_freq, i)
        sleep(0.01)
        print(i)
    sleep(0.1)

    for i in range(duty_m5deg, duty_p5deg, 10):
        pi.hardware_PWM(servo_pin, pwm_freq, i)
        sleep(0.01)
        print(i)
    sleep(0.1)

    for i in range(duty_p5deg, duty_0deg, -10):
        pi.hardware_PWM(servo_pin, pwm_freq, i)
        sleep(0.01)
        print(i)
    sleep(0.1)

    pi.hardware_PWM(servo_pin, pwm_freq, duty_0deg)
    pi.hardware_PWM(servo_pin, pwm_freq, 0)

def arm_calibration():

    global duty_arm_calib, duty_m5deg, duty_0deg, duty_p5deg
    duty = angle_dutyM(0)
    print(f'現在のduty比換算値: {duty}')
    pi.hardware_PWM(servo_pin, pwm_freq, duty)
    while True:
        n = int(input('アーム角度が0°になるようにduty比換算値を設定してください(変化量800で約1°の変化)[0で設定終了]: '))
        if (n >= angle_dutyM(-10)) & (n < angle_dutyM(10)):
            duty = n
            pi.hardware_PWM(servo_pin, pwm_freq, duty)
        elif n == 0:
            duty_arm_calib = duty - angle_dutyM(0)
            duty_m5deg = angle_dutyM(-5) + duty_arm_calib
            duty_p5deg = angle_dutyM(5) + duty_arm_calib
            duty_0deg = angle_dutyM(0) + duty_arm_calib
            return
        else:
            print(f'値は{angle_dutyM(-10)}から{angle_dutyM(10)}の間で設定してください')

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
    for i in range(100):
        distance = sensor.distance * 100
        print('Distance : %.2f' % distance)
        sleep(1)


def main():
    global duty_m5deg, duty_0deg, duty_p5deg
    duty_m5deg = angle_dutyM(-5)
    duty_p5deg = angle_dutyM(5)
    duty_0deg = angle_dutyM(0)
    #servo_test0()
    servo_test()
    #gyro_test()
    #dist_test()
    #servo_test90()
    arm_calibration()
    print(f'duty_arm_calib: {duty_arm_calib}')
    print(f'duty_m5deg: {duty_m5deg}')
    print(f'duty_0deg: {duty_0deg}')
    print(f'duty_p5deg: {duty_p5deg}')
    servo_test()    

if __name__ == '__main__':
    main()