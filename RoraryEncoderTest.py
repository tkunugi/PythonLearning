from gpiozero import RotaryEncoder, PWMLED
from gpiozero.tools import scaled_half
from time import sleep

rotary = RotaryEncoder(5,6)
led_red = PWMLED(21)
led_green = PWMLED(20)

def change(value):
    print(value)
    if value == 1:
        print('clockwise')
        led_red.on()
    else:
        print('counterclosewise')
        led_green.on()

while True:
    #rotary.when_rotated = change
    print(rotary.value)
    print(scaled_half(rotary.values))
    led_red.source = scaled_half(rotary.values)
    sleep(1)

