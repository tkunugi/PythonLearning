from gpiozero import Servo
from time import sleep

servo = Servo(16, min_pulse_width=0.5/1000, max_pulse_width=2.4/1000)

def main():
    while True:
        try:
            servo.min()
            sleep(1)
            servo.mid()
            sleep(1)
            servo.max()
            sleep(1)
            servo.mid()
            sleep(1)
            servo.min()
            sleep(1)
        except KeyboardInterrupt:
            print('fin')
            break

if __name__ == '__main__':
    main()
    

