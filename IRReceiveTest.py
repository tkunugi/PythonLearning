from gpiozero import Button
from time import sleep

button = Button(26, pull_up=True)

while True:
    #button.wait_for_press()
    #print('pressed')
    print(button.value)
    sleep(0.5)