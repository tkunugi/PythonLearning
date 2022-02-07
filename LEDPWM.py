from gpiozero import PWMLED
from time import sleep

led_red = PWMLED(23)

led_red.on()
sleep(1)
led_red.off()