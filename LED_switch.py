from gpiozero import LED, Button

led_red = LED(20)
led_green = LED(16)
led_blue = LED(12)
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
   