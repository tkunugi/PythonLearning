#from gpiozero import MotionSensor
from gpiozero import Button
from time import sleep

#pir = MotionSensor(21)
button = Button(5, pull_up=True)

while True:
#    pir.wait_for_motion()
    button.wait_for_press()
    print('Motion detected!')
    sleep(1)
    button.wait_for_release()
    print('Motion deactivated')
    sleep(1)