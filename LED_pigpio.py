from time import sleep
import pigpio

pig = pigpio.pi()
pig.set_mode(5, pigpio.OUTPUT)

try:
    while True:
        sleep(1)
        pig.write(5, 1)
        sleep(1)
        pig.write(5, 0)
except KeyboardInterrupt:
    pig.stop()