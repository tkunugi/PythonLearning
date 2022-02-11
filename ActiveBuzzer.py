from gpiozero import LED
from time import sleep

bz = LED(7)

bz.on()
sleep(1)
bz.off()

