from RPIO import PWM	#importamos a libreria para PWM
import time
import sys

SERVO_ERR = 3

pin_servo1 = 2
pin_servo2 = 3

def updateServo(pwm, angle):
	if angle<0 or angle>180:
	    angle = 90
	duty = float(angle) / 10.0 + 2.5
	pwm.ChangeDutyCycle(duty+SERVO_ERR)

#Miramos se existe un argumento de entrada utilizamolo como angulo
angle1 = 0
angle2 = 0
if len(sys.argv)>2:
	angle1 = int(sys.argv[1])
	angle2 = int(sys.argv[2])

pulso1 = angleToTime(angle1)
pulso2 = angleToTime(angle2)

print 'Pulso1: '+ repr(pulso1) +', Pulso2: '+ repr(pulso2)
servo=PWM.Servo()				#Iniciamos a libreria para o servo
servo.set_servo(pin_servo1,1500)		#Centramos o servo
servo.set_servo(pin_servo2,1500)
time.sleep(1)
servo.set_servo(pin_servo1,pulso1)
servo.set_servo(pin_servo2,pulso2)
time.sleep(1)
#servo.stop_servo(pin_servo1)
#servo.stop_servo(pin_servo2)
