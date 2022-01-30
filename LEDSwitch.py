from gpiozero import LED, Button


led_red = LED(2)
led_green = LED(3)
led_blue = LED(4)
button = Button(5, pull_up=False)

while True:
    button.wait_for_press()
    led_red.on()
    button.wait_for_release()
    
    button.wait_for_press()
    led_red.off()
    led_green.on()
    button.wait_for_release()
    
    button.wait_for_press()
    led_green.off()
    led_blue.on()
    button.wait_for_release()
    
    button.wait_for_press()
    led_blue.off()
    button.wait_for_release()
   