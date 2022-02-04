from gpiozero import LED, Button
from time import sleep


led_red = LED(20)

while True:
    led_red.on()
    sleep(1)
    led_red.off()
    sleep(1)