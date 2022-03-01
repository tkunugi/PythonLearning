import pigpio
from time import sleep
 
#RGBのポート番号の設定
GPIO_R = 16
GPIO_G = 20
GPIO_B = 21
 
FREQ = 50   #pwm周波数
RANGE = 100 #pwmの範囲
 
#pigpioの設定
pi = pigpio.pi()
 
p = [GPIO_R, GPIO_G, GPIO_B]
 
for i in range(3):
    pi.set_PWM_frequency(p[i],FREQ)
    pi.set_PWM_range(p[i],RANGE)
 
try:
    d = [0,0,0]
    r = [3,5,7]
    while True:
        sleep(0.1)
        for i in range(3):
            pi.set_PWM_dutycycle(p[i],d[i])
            d[i] += r[i]
            if d[i] >= RANGE or d[i] <= 0:
                r[i] *= -1
                d[i] += r[i]
except KeyboardInterrupt:
    pass
 
for i in range(3):
    pi.set_mode(p[i],pigpio.INPUT)
pi.stop()