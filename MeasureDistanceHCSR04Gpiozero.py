from turtle import distance
from gpiozero import DistanceSensor
from time import sleep

sensor = DistanceSensor(trigger = 5, echo = 6, max_distance=2.0)

while True:
    distance = sensor.distance * 100
    print('Distance : %.1f' % distance)
    sleep(1)
