import RPi.GPIO as GPIO
import time
import sys
import os
import errno
import math

SERVO_ERR = 3

GPIO_SERVO_X = 2
GPIO_SERVO_Y = 3
GPIO_LED = 4

VIDEO_RESOLUTION_X = 640 #1280
VIDEO_RESOLUTION_Y = 480 #720

VIDEO_ANGLE_X = 52.46 #35
VIDEO_ANGLE_Y = 30

AVERAGE_DEPTH_X = 73
AVERAGE_DEPTH_Y = 73

DEPTH_SIZE_X = math.tan(math.radians(VIDEO_ANGLE_X))*AVERAGE_DEPTH_X #95
DEPTH_SIZE_Y = 95

CAMERA_SEPARATION_X = 15
CAMERA_SEPARATION_Y = 0

FIFO = '/tmp/coordenadas'

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(GPIO_SERVO_X, GPIO.OUT)
GPIO.setup(GPIO_SERVO_Y, GPIO.OUT)
GPIO.setup(GPIO_LED, GPIO.OUT)

def updateServo(pwm, angle):
    if angle<0:
        angle=0
    elif angle>180:
        angle = 180
    duty = float(angle) / 10.0 + 2.5
    pwm.ChangeDutyCycle(duty+SERVO_ERR)

def coordToAngle(x,y):
    CENTER_X = VIDEO_RESOLUTION_X/2
    CENTER_Y = VIDEO_RESOLUTION_Y/2
    coordX = float(x-CENTER_X)
    coordY = float(CENTER_Y-y)
    x = float(x)
    y = float(y)

    PosX = (x/VIDEO_RESOLUTION_X)*DEPTH_SIZE_X
    #PosY = (y/VIDEO_RESOLUTION_Y)*DEPTH_SIZE_Y

    desp_x = (float(DEPTH_SIZE_X)/2)-CAMERA_SEPARATION_X
    #desp_y = (DEPTH_SIZE_Y/2)-CAMERA_SEPARATION_Y

    angleX = math.degrees(math.atan(abs(PosX-desp_x)/AVERAGE_DEPTH_X))
    #angleY = math.degrees(math.atan(abs(PosY-desp_y)/AVERAGE_DEPTH_Y))

    angleX = 90-angleX if (PosX >= desp_x) else 90+angleX
    #angleY = 90-angleY if (PosY >= desp_y) else 90+angleY

    angleY = (coordY/float(CENTER_Y))*VIDEO_ANGLE_Y

    return angleX, angleY

    #return (coordX/float(CENTER_X))*VIDEO_ANGLE_X, (coordY/float(CENTER_Y))*VIDEO_ANGLE_Y

def receiveCoords():
	try:
	    os.mkfifo(FIFO)
	except OSError as oe:
	    if oe.errno != errno.EEXIST:
	        raise
	with open(FIFO) as fifo:
	    time.sleep(.1)
	    data = fifo.read()
	    if len(data) == 0:
		return -1, -1
            Sx = data.split('-')[0]
	    Sy = data.split('-')[1]
	    x = Sx.split(':', 1)[1]
	    y = Sy.split(':', 1)[1]
            print(x,y)
	    return int(x), int(y)


#Miramos se existe un argumento de entrada utilizamolo como angulo
coordX = 0
coordY = 0
if len(sys.argv)>2:
    coordX = int(sys.argv[1])
    coordY = int(sys.argv[2])
    # coordToAngle(coordX, coordY)
    # sys.exit(1)

pwm_X = GPIO.PWM(GPIO_SERVO_X, 100)
pwm_Y = GPIO.PWM(GPIO_SERVO_Y, 100)
pwm_X.start(1)
pwm_Y.start(1)

updateServo(pwm_X, 90-9)
updateServo(pwm_Y, 90)
time.sleep(0.5)
pwm_X.ChangeDutyCycle(0);
pwm_Y.ChangeDutyCycle(0);

while True:

    try:

        coordX, coordY = receiveCoords()

        print(coordX,coordY)

        coordX = coordX if coordX>0 else 0
        coordY = coordY if coordY>0 else 0
        coordX = coordX if coordX<VIDEO_RESOLUTION_X else VIDEO_RESOLUTION_X
        coordY = coordY if coordY<VIDEO_RESOLUTION_Y else VIDEO_RESOLUTION_Y

        angleX, angleY = coordToAngle(coordX, coordY)
        angleX = 90 - angleX
        angleY = 90 - angleY
        print angleX," - ", angleY

        updateServo(pwm_X, angleX-9)
        updateServo(pwm_Y, angleY)

        time.sleep(0.5)

        GPIO.output(GPIO_LED, GPIO.HIGH)
        pwm_X.ChangeDutyCycle(0);
        pwm_Y.ChangeDutyCycle(0);

        time.sleep(1)

        GPIO.output(GPIO_LED, GPIO.LOW)

    except KeyboardInterrupt:
        break

print "Pulse [Enter] para terminar."
s = sys.stdin.read(1)

updateServo(pwm_X, 90-9)
updateServo(pwm_Y, 90)
time.sleep(.5)
