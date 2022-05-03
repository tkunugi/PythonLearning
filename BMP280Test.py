from time import sleep
from bme280 import bme280
from bme280 import bme280_i2c

bme280_i2c.set_default_i2c_address(0x76)
bme280_i2c.set_default_bus(1)

bme280.setup()

while True:
    data_all = bme280.read_all()

    print('%7.2f C' % data_all.temperature)
    print('%7.2f %%' % data_all.humidity)
    print('%7.2f hPa' % data_all.pressure)
    sleep(1)
    