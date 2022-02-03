
# from gpiozero import DigitalInputDevice
import RPi.GPIO as GPIO
import dht11
import time
import datetime

# initialize GPIO
GPIO.setwarnings(True)
GPIO.setmode(GPIO.BCM)
# read data using pin 4,5
instance = dht11.DHT11(pin=14)
#d0_input = DigitalInputDevice(5)
try:
    while True:
        result = instance.read()
        #print(result, result.temperature)
        if result.is_valid():
            print("Last valid input: " + str(datetime.datetime.now()))
            print("Temperature: %-3.1f C" % result.temperature)
            print("Humidity: %-3.1f %%" % result.humidity)
            # print('OK')
       
       
#　　if (not d0_input.value):
#　　　print('Ground humidity: enough')
#　　else:
#　　　print('Ground humidity: need')
       
            time.sleep(1)   
except KeyboardInterrupt:
    print("Cleanup")
    GPIO.cleanup()