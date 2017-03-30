import RPi.GPIO as GPIO
import time
import sys
import os
import errno

SERVO_ERR = 3

GPIO_SERVO_X = 2
GPIO_SERVO_Y = 3
GPIO_LED = 4

VIDEO_RESOLUTION_X = 1280
VIDEO_RESOLUTION_Y = 720

VIDEO_ANGLE_X = 40
VIDEO_ANGLE_Y = 40

FIFO = '/tmp/coordenadas'

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(GPIO_SERVO_X, GPIO.OUT)
GPIO.setup(GPIO_SERVO_Y, GPIO.OUT)
GPIO.setup(GPIO_LED, GPIO.OUT)

def updateServo(pwm, angle):
	if angle<0 or angle>180:
	    angle = 90
	duty = float(angle) / 10.0 + 2.5
	pwm.ChangeDutyCycle(duty+SERVO_ERR)

def coordToAngle(x,y):
	CENTER_X = VIDEO_RESOLUTION_X/2
	CENTER_Y = VIDEO_RESOLUTION_Y/2
	coordX = float(x-CENTER_X)
	coordY = float(CENTER_Y-y)
	return (coordX/float(CENTER_X))*VIDEO_ANGLE_X, (coordY/float(CENTER_Y))*VIDEO_ANGLE_Y

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
		return int(x), int(y)


#Miramos se existe un argumento de entrada utilizamolo como angulo
coordX = 0
coordY = 0
# if len(sys.argv)>2:
# 	coordX = int(sys.argv[1])
# 	coordY = int(sys.argv[2])

pwm_X = GPIO.PWM(GPIO_SERVO_X, 100)
pwm_Y = GPIO.PWM(GPIO_SERVO_Y, 100)
pwm_X.start(1)
pwm_Y.start(1)

updateServo(pwm_X, 90)
updateServo(pwm_Y, 90)
time.sleep(0.5)

while True:

	try:

		coordX, coordY = receiveCoords()

		coordX = coordX if coordX>0 else 0
		coordY = coordY if coordY>0 else 0
		coordX = coordX if coordX<VIDEO_RESOLUTION_X else VIDEO_RESOLUTION_X
		coordY = coordY if coordY<VIDEO_RESOLUTION_Y else VIDEO_RESOLUTION_Y

		angleX, angleY = coordToAngle(coordX, coordY)
		angleX = 90 - angleX
		angleY = 90 - angleY
		print angleX," - ", angleY

		updateServo(pwm_X, angleX)
		updateServo(pwm_Y, angleY)

        GPIO.output(GPIO_LED, GPIO.HIGH)

		time.sleep(1)

		GPIO.output(GPIO_LED, GPIO.LOW)


	except KeyboardInterrupt:
            break

print "Pulse [Enter] para terminar."
s = sys.stdin.read(1)

updateServo(pwm_X, 90)
updateServo(pwm_Y, 90)
time.sleep(.5)
