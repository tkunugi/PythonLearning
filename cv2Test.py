import cv2

img = cv2.imread('/home/pi/Documents/python/data/300x200.bmp', flags=cv2.IMREAD_GRAYSCALE)
cv2.imshow('Simulation', img)

while True:
    pass