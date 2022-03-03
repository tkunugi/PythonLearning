from gpiozero import LED, Button
from time import sleep

led_red = LED(16)
button = Button(20, pull_up=True)

while True:
    button.wait_for_press()
    led_red.on()
    button.wait_for_release()
    led_red.off()
    
   