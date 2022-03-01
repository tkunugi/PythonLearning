import pigpio

pi = pigpio.pi()
pi.set_mode(16, pigpio.OUTPUT)
pi.set_mode(20, pigpio.OUTPUT)
pi.set_mode(21, pigpio.OUTPUT)

pi.write(16,0)
pi.write(20,0)
pi.write(21,0)