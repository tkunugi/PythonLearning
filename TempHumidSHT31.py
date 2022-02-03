from logging import exception
import time
import smbus
import csv
import datetime
import requests

def tempChanger(msb, lsb):
    mlsb = ((msb << 8) | lsb) 
    return (-45 + 175 * int(str(mlsb), 10) / (pow(2, 16) - 1)) 

def humidChanger(msb, lsb):
    mlsb = ((msb << 8) | lsb)
    return (100 * int(str(mlsb), 10) / (pow(2, 16) - 1))

i2c = smbus.SMBus(1)
i2c_addr = 0x45    

i2c.write_byte_data(i2c_addr, 0x21, 0x30) 
time.sleep(0.5)

f = open('../data/TempHumid.csv', 'w')
writer = csv.writer(f, lineterminator = '\n')



try:
    while True:
        i2c.write_byte_data(i2c_addr, 0xE0, 0x00)   
        data = i2c.read_i2c_block_data(i2c_addr, 0x00, 6) 
        temperature = tempChanger(data[0], data[1])
        temperature_f = '{:.4g}'.format(temperature)
        print(temperature_f)
        humidity = humidChanger(data[3], data[4])
        humidity_f= '{:.4g}'.format(humidity)
        print(humidity_f)
        now = datetime.datetime.now()
        now_f = now.strftime("%Y/%m/%d %H:%M:%S")
        print(now_f)
        writer.writerow([now_f, temperature_f, humidity_f])
        url = 'https://script.google.com/macros/s/AKfycbwCgxqw5_8ekFvgvo_u3lXx5NtA1Dv8USV0xcFH3RudTydPFifEEEIzPg3NRj6ApJUVUw/exec?date_now={}&t={}&h={}'.format(now_f, temperature_f, humidity_f)
        requests.get(url)
        #print( str('{:.4g}'.format(tempChanger(data[0], data[1]))) + "C" )
        #print( str('{:.4g}'.format(humidChanger(data[3], data[4]))) + "%" )
        #print("------")
        time.sleep(60)
except KeyboardInterrupt:
    print('closed')
    f.closed

