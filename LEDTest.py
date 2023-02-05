from gpiozero import LED, Button
from time import sleep

led_red = LED(12)
led_green = LED(16)
led_blue = LED(20)


while True:
    led_red.on()
    sleep(1)
    led_red.off()
    led_green.on()
    sleep(1)
    led_green.off()
    led_blue.on()
    sleep(1)
    led_blue.off()
    sleep(1)