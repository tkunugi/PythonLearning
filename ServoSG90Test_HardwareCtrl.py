import pigpio
from time import sleep

gpio_pin = 18

pi = pigpio.pi()
pi.set_mode(gpio_pin, pigpio.OUTPUT)
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

for i in range(0, -90, -3):
    pi.hardware_PWM(gpio_pin, pwm_freq, angle_dutyM(i))
    sleep(0.1)
    print(i)

for i in range(-90, 90, 3):
    pi.hardware_PWM(gpio_pin, pwm_freq, angle_dutyM(i))
    sleep(0.1)
    print(i)

for i in range(90, 0, -3):
    pi.hardware_PWM(gpio_pin, pwm_freq, angle_dutyM(i))
    sleep(0.1)
    print(i)

pi.hardware_PWM(gpio_pin, pwm_freq, 0)
pi.stop()


