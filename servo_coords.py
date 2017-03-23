# from RPIO import PWM	#importamos a libreria para PWM
import time
import sys

SERVO_ERR = 3

GPIO_SERVO_X = 2
GPIO_SERVO_Y = 3

VIDEO_RESOLUTION_X = 1280
VIDEO_RESULUTION_Y = 720

VIDEO_ANGLE_X = 40
VIDEO_ANGLE_Y = 40

# GPIO.setmode(GPIO.BCM)
# GPIO.setwarnings(False)
#
# GPIO.setup(GPIO_SERVO_X, GPIO.OUT)
# GPIO.setup(GPIO_SERVO_Y, GPIO.OUT)

def updateServo(pwm, angle):
	if angle<0 or angle>180:
	    angle = 90
	duty = float(angle) / 10.0 + 2.5
	pwm.ChangeDutyCycle(duty+SERVO_ERR)

def coordToAngle(x,y):
	CENTER_X = VIDEO_RESOLUTION_X/2
	CENTER_Y = VIDEO_RESULUTION_Y/2
	coordX = float(x-CENTER_X)
	coordY = float(CENTER_Y-y)
	return (coordX/float(CENTER_X))*VIDEO_ANGLE_X, (coordY/float(CENTER_Y))*VIDEO_ANGLE_Y

#Miramos se existe un argumento de entrada utilizamolo como angulo
coordX = 0
coordY = 0
if len(sys.argv)>2:
	coordX = int(sys.argv[1])
	coordY = int(sys.argv[2])

# pwm_X = GPIO.PWM(GPIO_SERVO_X, 100)
# pwm_Y = GPIO.PWM(GPIO_SERVO_Y, 100)
# pwm_X.start(5)
# pwm_Y.start(5)

angleX, angleY= normalizeAndCenter(coordX, coordY)
print angleX," - ", angleY
exit(1)

updateServo(pwm_X, angleX)
updateServo(pwm_Y, angleY)
time.sleep(1)
print "Pulse [Enter] para terminar."
s = sys.stdin.read(1)

updateServo(pwm_X, 90)
updateServo(pwm_Y, 90)
time.sleep(.5)
pwm1.stop()
pwm2.stop()
