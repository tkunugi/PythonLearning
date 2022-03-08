from picamera import PiCamera
from time import sleep

camera = PiCamera()

camera.start_preview()
#for i in range(5):
#    sleep(5)
#    camera.capture('/home/pi/Images/image%s.jpg' % i)
camera.start_recording('/home/pi/Videos/video.h264')
sleep(5)
camera.stop_recording()
camera.stop_preview()