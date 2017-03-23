from RPIO import PWM	#importamos a libreria para PWM
import time
import sys

SERVO_ERR = 3

GPIO_SERVO1 = 2
GPIO_SERVO2 = 3

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(GPIO_SERVO1, GPIO.OUT)
GPIO.setup(GPIO_SERVO2, GPIO.OUT)

def updateServo(pwm, angle):
	if angle<0 or angle>180:
	    angle = 90
	duty = float(angle) / 10.0 + 2.5
	pwm.ChangeDutyCycle(duty+SERVO_ERR)

#Miramos se existe un argumento de entrada utilizamolo como angulo
angle1 = 90
angle2 = 90
if len(sys.argv)>2:
	angle1 = int(sys.argv[1])
	angle2 = int(sys.argv[2])

pwm1 = GPIO.PWM(GPIO_SERVO1, 100)
pwm2 = GPIO.PWM(GPIO_SERVO2, 100)
pwm1.start(5)
pwm2.start(5)

updateServo(pwm1, angle1)
updateServo(pwm2, angle2)
time.sleep(1)
print "Pulse [Enter] para terminar."
s = sys.stdin.read(1)

updateServo(pwm1, 90)
updateServo(pwm2, 90)
time.sleep(.5)
pwm1.stop()
pwm2.stop()
