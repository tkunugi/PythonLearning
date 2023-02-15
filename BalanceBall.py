import numpy as np
import pandas as pd
import datetime
from time import sleep
from gpiozero import DistanceSensor
from mpu6050 import mpu6050
import pigpio

sensor_gyro = mpu6050(0x68)
sensor = DistanceSensor(trigger = 20, echo = 21, max_distance=2.0)

servo_pin = 18
duty_arm_calib = 0  #アームの初期角度補正用


pi = pigpio.pi()
pi.set_mode(servo_pin, pigpio.OUTPUT)
pwm_freq = 50   #SC90のPWMサイクル数
time_m90 = 0.5  #-90°のときのパルス時間
time_p90 = 2.4  #+90°のときのパルス時間

pwm_period = 1000 / pwm_freq  #PWM周期時間(msec)
dutyM_m90_raw = 1e+6 * time_m90 / pwm_period  #-90°のときのduty比(100%は1,000,000)、角度補正なし
dutyM_p90_raw = 1e+6 * time_p90 / pwm_period  #-90°のときのduty比(100%は1,000,000)、角度補正なし

def angle_dutyM_nocalib(deg):
    #角度(°)から、duty比(100%は1,000,000)に換算
    dutyM = int(dutyM_m90_raw + (dutyM_p90_raw - dutyM_m90_raw) * ((deg + 90.) / 180.))
    return dutyM

def angle_dutyM(deg):
    dutyM = angle_dutyM_nocalib(deg) + duty_arm_calib
    return dutyM

def servo_test90():
    #サーボモーターの駆動テスト用(アームなしでのテスト用) -0°→ -90° → +90° → 0°
    for i in range(0, -90, -3):
        pi.hardware_PWM(servo_pin, pwm_freq, angle_dutyM_nocalib(i))
        sleep(0.1)
        #print(i)
    sleep(0.1)

    for i in range(-90, 90, 3):
        pi.hardware_PWM(servo_pin, pwm_freq, angle_dutyM_nocalib(i))
        sleep(0.1)
        #print(i)
    sleep(0.1)

    for i in range(90, 0, -3):
        pi.hardware_PWM(servo_pin, pwm_freq, angle_dutyM_nocalib(i))
        sleep(0.1)
        #print(i)
    sleep(0.1)

    pi.hardware_PWM(servo_pin, pwm_freq, 0)

def servo_test0():
    #サーボモーターの駆動テスト用(アームありでのテスト用) -0°→ -5° → +5° → 0°
    for i in np.arange(0., -5., -1):
        pi.hardware_PWM(servo_pin, pwm_freq, angle_dutyM_nocalib(i))
        sleep(0.1)
        pi.hardware_PWM(servo_pin, pwm_freq, 0)
        sleep(1)
        print(i)
    sleep(0.1)

    for i in np.arange(-5., 5., 1):
        pi.hardware_PWM(servo_pin, pwm_freq, angle_dutyM_nocalib(i))
        sleep(0.1)
        pi.hardware_PWM(servo_pin, pwm_freq, 0)
        sleep(1)
        print(i)
    sleep(0.1)

    for i in np.arange(5., 0., -1):
        pi.hardware_PWM(servo_pin, pwm_freq, angle_dutyM_nocalib(i))
        sleep(0.1)
        pi.hardware_PWM(servo_pin, pwm_freq, 0)
        sleep(1)
        print(i)
    sleep(0.1)

    pi.hardware_PWM(servo_pin, pwm_freq, 0)
    pi.stop()

def servo_test():
    #サーボモーターの駆動テスト用(アームありでのテスト用) -0°→ -5° → +5° → 0°
    # 角度変換関数を関数実行直後に使用し、その後直接数値で駆動することにより高速化を図った
    
    for i in range(angle_dutyM(0.), angle_dutyM(-5.), -100):
        pi.hardware_PWM(servo_pin, pwm_freq, i)
        sleep(0.1)
        print(i)
    sleep(0.1)

    for i in range(angle_dutyM(-5.), angle_dutyM(5.), 100):
        pi.hardware_PWM(servo_pin, pwm_freq, i)
        sleep(0.1)
        print(i)
    sleep(0.1)

    for i in range(angle_dutyM(5.), angle_dutyM(0.), -100):
        pi.hardware_PWM(servo_pin, pwm_freq, i)
        sleep(0.1)
        print(i)
    sleep(0.1)

    pi.hardware_PWM(servo_pin, pwm_freq, angle_dutyM(0.))
    pi.hardware_PWM(servo_pin, pwm_freq, 0)

def arm_calibration():

    global duty_arm_calib #, duty_m5deg, duty_0deg, duty_p5deg
    duty = angle_dutyM_nocalib(0)
    print(f'現在のduty比換算値: {duty}')
    pi.hardware_PWM(servo_pin, pwm_freq, duty)
    while True:
        n_in = input('アーム角度が0°になるようにduty比換算値を設定してください(変化量800で約1°の変化)[0で設定終了]: ')
        if n_in.isdigit() == False:
            print('数値を入力してください')
            continue
        n = int(n_in)
        if (n >= angle_dutyM_nocalib(-10)) & (n < angle_dutyM_nocalib(10)):
            duty = n
            pi.hardware_PWM(servo_pin, pwm_freq, duty)
        elif n == 0:
            duty_arm_calib = duty - angle_dutyM_nocalib(0)
            pi.hardware_PWM(servo_pin, pwm_freq, 0)
            return
        else:
            print(f'値は{angle_dutyM_nocalib(-10)}から{angle_dutyM_nocalib(10)}の間で設定してください')

def gyro_test():
    #ジャイロセンサーのテスト 読み取り値を1秒ごとに3回表示
    for i in range(3):
        gyro_data = sensor_gyro.get_gyro_data()
        accel_data = sensor_gyro.get_accel_data()

        print(' Gyro x:' + '{:04f}'.format(gyro_data['x']) + ' y:' + '{:04f}'.format(gyro_data['y']) + ' z:' + '{:04f}'.format(gyro_data['z']))
        print(' Accel x:' + '{:04f}'.format(accel_data['x']) + ' y:' + '{:04f}'.format(accel_data['y']) + ' z:' + '{:04f}'.format(accel_data['z']))
    
        sleep(1)

def dist_test():
    #距離センサーのテスト 読み取り値を1秒ごとに3回表示
    for i in range(30):
        distance = sensor.distance * 100
        print('Distance : %.2f' % distance)
        sleep(1)

def get_move_response():
    
    data = pd.DataFrame(columns=['datetime', 'duty', 'distance'])
    columns = data.columns

    while True:
        n = input('何秒間試験をしますか (1〜6000秒)? ')
        if n.isdigit() == False:
            print('数値を入力してください')
            continue
        elif ((int(n) <= 1) or ( int(n) >= 6000)):
            print('1〜6000の間で入力してください')
            continue
        else:
            test_time = int(n) * 10 #試験時間を0.1秒を単位として設定
            break
    
    n = input('球をアームの中央付近に置いてください [OK: Enter, Quit:Q] ')
    if (n == 'Q') or (n == 'q'):
        return
    
    '''
    #アームが−1〜+1° → -2〜+2° → -3〜+3°と振れていき、ボールの位置を取得する
    for max_angle in range(1, 3):
        
        for i in range(angle_dutyM(0.), angle_dutyM(float(max_angle * -1)), -10):
            pi.hardware_PWM(servo_pin, pwm_freq, i)
            dist = sensor.distance * 100
            datum = pd.DataFrame([[datetime.datetime.now(), i, dist]], columns=columns)
            data = data.append(datum, ignore_index=True)
            sleep(0.01)
            print(i)
        sleep(0.1)

        for i in range(angle_dutyM(float(max_angle * -1)), angle_dutyM(float(max_angle)), 10):
            pi.hardware_PWM(servo_pin, pwm_freq, i)
            dist = sensor.distance * 100
            datum = pd.DataFrame([[datetime.datetime.now(), i, dist]], columns=columns)
            data = data.append(datum, ignore_index=True)
            sleep(0.01)
            print(i)
        sleep(0.1)

        for i in range(angle_dutyM(float(max_angle)), angle_dutyM(0.), -10):
            pi.hardware_PWM(servo_pin, pwm_freq, i)
            dist = sensor.distance * 100
            datum = pd.DataFrame([[datetime.datetime.now(), i, dist]], columns=columns)
            data = data.append(datum, ignore_index=True)
            sleep(0.01)
            print(i)
        sleep(0.1)
    '''
    #
    duty_limit_max = angle_dutyM(5.)  #アーム振れ角の最大のデューティ比
    duty_limit_min = angle_dutyM(-5.) #アーム振れ角の最小のデューティ比
    a1 = -1.                          #比例制御係数
    dist_pre = 20 #距離測定が異常の際に前回値を使うための変数
    
    duty = angle_dutyM(0.)

    for i in range(test_time):
        pi.hardware_PWM(servo_pin, pwm_freq, duty)
        dist_raw = sensor.distance * 100
        dist = dist_raw if (dist_raw <= 40) & (dist_raw >= 0) else dist_pre
        dist_pre = dist
        datum = pd.DataFrame([[datetime.datetime.now(), i, dist]], columns=columns)
        data = data.append(datum, ignore_index=True)
        print(f'#{i} Distance:{dist} Distance(raw)]{dist_raw} Duty:{duty}')
        duty += int((dist - 20.) * a1)
        duty = duty_limit_max if duty > duty_limit_max else duty
        duty = duty_limit_min if duty < duty_limit_min else duty
        sleep(0.1)
    
    pi.hardware_PWM(servo_pin, pwm_freq, angle_dutyM(0.))
    pi.hardware_PWM(servo_pin, pwm_freq, 0)

    file_name = '../data/ball_balance_' + datetime.datetime.now().strftime('%Y%m%d%H%M%s') + '.csv'
    data.to_csv(file_name)


def menu():

    while True:   
        print('1: サーボ駆動テスト(-90°〜+90°、アーム接続なし')
        print('2: サーボ駆動テスト(-5°〜+5°)')
        print('3: ジャイロセンサ動作テスト')
        print('4: 距離センサ動作テスト')
        print('5: アーム角度0°設定')
        print('9: 試験動作実行')
        print('Q: 終了')
        menu = input('何番を起動しますか? ')
        if menu == '1':
            servo_test90()
        elif menu == '2':
            servo_test()
        elif menu == '3':
            gyro_test()
        elif menu == '4':
            dist_test()
        elif menu == '5':
            arm_calibration()
            print(f'duty_arm_calib: {duty_arm_calib}')
        elif menu == '9':
            get_move_response()
        elif (menu == 'Q') or (menu == 'q'):
            break
        else:
            print('メニューの番号を入力してください')

if __name__ == '__main__':
    menu()
