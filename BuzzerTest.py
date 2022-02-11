from gpiozero import Buzzer
from time import sleep

bz = Buzzer(7)

def buzz(pitch, duration):
    period = 1.0 / pitch
    delay = period / 2
    cycles = int(duration * pitch)
    bz.beep(on_time=period, off_time=period, n=int(cycles/2))

while True:
    pitch_s = input('Pich (200 to 2000): ')
    pitch = float(pitch_s)
    duration_s = input('Duration (sec): ')
    duration = float(duration_s)
    buzz(pitch, duration)


