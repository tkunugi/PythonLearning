from gpiozero import DistanceSensor
from time import sleep

sensor = DistanceSensor(trigger = 20, echo = 21, max_distance=2.0)

while True:
    distance = sensor.distance * 100
    print('Distance : %.1f' % distance)
    sleep(1)
