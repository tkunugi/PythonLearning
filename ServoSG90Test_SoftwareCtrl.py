from gpiozero import AngularServo
from time import sleep

servo = AngularServo(18, min_pulse_width=0.5/1000, max_pulse_width=2.4/1000)

for i in list(range(0,-90, -1)):
    servo.angle = i
    sleep(0.1)

for i in list(range(-90,90)):
    servo.angle = i
    sleep(0.1)

for i in list(range(90, 0,-1)):
    servo.angle = i
    sleep(0.1)

