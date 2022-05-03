from logging import exception
from time import sleep
import smbus
import csv
import datetime
import requests
from ccs811 import CCS811
from bme280 import bme280
from bme280 import bme280_i2c

bme280_i2c.set_default_i2c_address(0x76)
bme280_i2c.set_default_bus(1)


def tempChanger(msb, lsb):
    mlsb = ((msb << 8) | lsb) 
    return (-45 + 175 * int(str(mlsb), 10) / (pow(2, 16) - 1)) 

def humidChanger(msb, lsb):
    mlsb = ((msb << 8) | lsb)
    return (100 * int(str(mlsb), 10) / (pow(2, 16) - 1))


class CCS811Monitor:
    CO2_PPM_THRESHOLD_1 = 1000
    CO2_PPM_THRESHOLD_2 = 2000

    CO2_LOWER_LIMIT  =  400
    CO2_HIGHER_LIMIT = 8192

    CO2_STATUS_CONDITIONING = 'CONDITIONING'
    CO2_STATUS_LOW          = 'LOW'
    CO2_STATUS_HIGH         = 'HIGH'
    CO2_STATUS_TOO_HIGH     = 'TOO HIGH'
    CO2_STATUS_ERROR        = 'ERROR'

    def __init__(self):
        self._ccs811 = CCS811()

    def status(self, co2):
        if co2 < self.CO2_LOWER_LIMIT or co2 > self.CO2_HIGHER_LIMIT:
            return self.CO2_STATUS_CONDITIONING
        elif co2 < self.CO2_PPM_THRESHOLD_1:
            return self.CO2_STATUS_LOW
        elif co2 < self.CO2_PPM_THRESHOLD_2:
            return self.CO2_STATUS_HIGH
        else:
            return self.CO2_STATUS_TOO_HIGH

    def ccs811print(self):
        #while not self._ccs811.available():
        #    pass

        #while True:
        #if not self._ccs811.available():
        #    sleep(1)
        #    continue

        try:
            #print('ccs811print')
            #print('reaData', self._ccs811.readData())
            if not self._ccs811.readData():
                #print('not css811 readData')
                co2 = self._ccs811.geteCO2()
                #print('co2', co2)
                co2_status = self.status(co2)
                print('co2status', co2_status)
                if co2_status == self.CO2_STATUS_CONDITIONING:
                    print("Under Conditioning...")
                    #self._logger.debug("Under Conditioning...")
                    sleep(2)
                    #continue
                tvoc = self._ccs811.getTVOC()
                #print("CO2: {0}ppm, TVOC: {1}".format(co2, tvoc))
                
                #print('self.co2_status', self.co2_status)

                #if co2_status != self.co2_status:
                #    self.co2_status = co2_status
                #    #self._logger.info("CO2: {0}ppm, TVOC: {1}".format(co2, self._ccs811.getTVOC()))

                return co2, tvoc
            else:
                #self._logger.error('ERROR!')
                #print('ccs811 readData')
                while True:
                    pass
        except:
            #self._logger.error(sys.exc_info())
            print('except')
            pass
        #sleep(2)


sht31 = smbus.SMBus(1)
sht31_addr = 0x45    

sht31.write_byte_data(sht31_addr, 0x21, 0x30) 
sleep(0.5)

ccs811 = CCS811Monitor()

bme280.setup()

#f = open('../data/TempHumid.csv', 'w')
#writer = csv.writer(f, lineterminator = '\n')



try:
    while True:
        sht31.write_byte_data(sht31_addr, 0xE0, 0x00)   
        data = sht31.read_i2c_block_data(sht31_addr, 0x00, 6) 
        temperature = tempChanger(data[0], data[1])
        temperature_f = '{:.4g}'.format(temperature)
        print(temperature_f)
        humidity = humidChanger(data[3], data[4])
        humidity_f= '{:.4g}'.format(humidity)
        print(humidity_f)
        now = datetime.datetime.now()
        now_f = now.strftime("%Y/%m/%d %H:%M:%S")
        print(now_f)

        css811_return = ccs811.ccs811print()
        #print('co2, tvoc: ', css811_return)
        co2_f = str(css811_return[0])
        
        
        tvoc_f = str(css811_return[1])
        #co2_f = '{:.4g}'.format(510)
        #tvoc_f = '{:.4g}'.format(100)
        #co2_f = 510
        #tvoc_f = 100

        print('co2, tvoc: ', co2_f, tvoc_f)

        data_all = bme280.read_all()

        temperature2_f = '{:.4g}'.format(data_all.temperature)
        pressure_f = '{:.6g}'.format(data_all.pressure)
        print(temperature2_f, pressure_f)

        #writer.writerow([now_f, temperature_f, humidity_f])
        #url = 'https://script.google.com/macros/s/AKfycbwCgxqw5_8ekFvgvo_u3lXx5NtA1Dv8USV0xcFH3RudTydPFifEEEIzPg3NRj6ApJUVUw/exec?date_now={}&t={}&h={}'.format(now_f, temperature_f, humidity_f)
        #url = 'https://script.google.com/macros/s/AKfycbwCgxqw5_8ekFvgvo_u3lXx5NtA1Dv8USV0xcFH3RudTydPFifEEEIzPg3NRj6ApJUVUw/exec?date_now={}&t={}&h={}&co={}&v={}'.format(now_f, temperature_f, humidity_f, co2_f, tvoc_f)
        url = 'https://script.google.com/macros/s/AKfycbwCgxqw5_8ekFvgvo_u3lXx5NtA1Dv8USV0xcFH3RudTydPFifEEEIzPg3NRj6ApJUVUw/exec?date_now={}&t={}&h={}&co={}&v={}&p={}'.format(now_f, temperature_f, humidity_f, co2_f, tvoc_f, pressure_f)
        requests.get(url)
        #print( str('{:.4g}'.format(tempChanger(data[0], data[1]))) + "C" )
        #print( str('{:.4g}'.format(humidChanger(data[3], data[4]))) + "%" )
        #print("------")
        sleep(60)
except KeyboardInterrupt:
    print('closed')
    #f.closed
 
