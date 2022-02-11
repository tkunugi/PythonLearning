from gpiozero import TonalBuzzer
from time import sleep

bz = TonalBuzzer(7)
bz.play('A4')
sleep(0.5)
bz.play('B4')
sleep(0.5)
bz.play('C5')
sleep(0.5)
bz.stop()
