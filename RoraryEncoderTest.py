from gpiozero import RotaryEncoder, PWMLED
from gpiozero.tools import scaled_half, scaled
from time import sleep

rotary = RotaryEncoder(5,6)
led_red  = PWMLED(23)
led_green = PWMLED(24)

def change(value):
    print('value: ', value)
    if value == 1:
        print('clockwise')
        #led_red.on()
    else:
        print('counterclosewise')
        #led_green.on()

def rotary_rotated_cw():
    print('clockwise')

def rotary_rotated_ccw():
    print('counterclosewise')
    

while True:
    #rotary.when_rotated = change
    rotary.when_rotated_clockwise = rotary_rotated_cw
    rotary.when_rotated_counter_clockwise = rotary_rotated_ccw
    print('rotary value', rotary.value)
    #led_red.source = scaled_half(rotary.values)
    #led_red.value = rotary.value

    if rotary.value >= 0:
        led_red.value = rotary.value
        led_green.off()
    else:
        led_green.value = - rotary.value
        led_red.off()

    sleep(0.25)

