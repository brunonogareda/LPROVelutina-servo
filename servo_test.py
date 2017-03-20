from RPIO import PWM    #importamos a libreria para PWM
import time
import sys

pin_servo1 = 2
pin_servo2 = 3

#Esta funcion calcula o tempo de activacion do pulso en us en funcion do angulo que se lle pasa.
def angleToTime(angulo):
        if angulo<=90 and angulo>=-90:
                return (((90.0+angulo)*(50.0/9.0))+1000)
        else:
                return 1500

#Miramos se existe un argumento de entrada utilizamolo como angulo
angle1 = 0
angle2 = 0
if len(sys.argv)>2:
        angle1 = int(sys.argv[1])
        angle2 = int(sys.argv[2])

pulso1 = angleToTime(angle1)
pulso2 = angleToTime(angle2)

print 'Pulso1: '+ repr(pulso1) +', Pulso2: '+ repr(pulso2)
servo=PWM.Servo()                               #Iniciamos a libreria para o servo


servo.set_servo(pin_servo2,1500)
servo.set_servo(pin_servo1,1500)                #Centramos o servo
time.sleep(1)
for _i in range(50):
    servo.set_servo(pin_servo1,590)
    servo.set_servo(pin_servo2,590)
    time.sleep(1)
    servo.set_servo(pin_servo1,2200)
    servo.set_servo(pin_servo2,2200)
    time.sleep(1)

servo.stop_servo(pin_servo1)
servo.stop_servo(pin_servo2)
