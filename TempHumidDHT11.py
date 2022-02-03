#2022-2-3 Adafruit_DHTライブラリをインストールできていないので本コードは動かせていない

# csvfile = "/home/pi/My-logs/temp_181.txt"

import time
from datetime import datetime

import Adafruit_DHT


pin_dht11 = 4 # GPIO number-color brown

while True:
    date = datetime.now()
    timestamp = date.strftime("%d/%m/%Y %H:%M:%S")

    #Read the DHT11 device to get humidity and temperature
    hum_dht11, temp_dht11 = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, pin_dht11)

    values_10 = timestamp,  round(temp_dht11, 1), round(hum_dht11, 1)

    #with open(csvfile, "a") as f:
    #    f.write (str(values_10) + "\n")

    print(values_10)
    #f.close()
    #time.sleep(10)