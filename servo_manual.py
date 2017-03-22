import RPi.GPIO as GPIO
import math
import xbox
from subprocess import call #Importamos para a interrupcion de teclado
import time

SERVO_ERR = 3

GPIO_LED_GREEN  = 23
GPIO_LED_RED    = 22
GPIO_LED_YELLOW = 27
GPIO_LED_BLUE   = 17

GPIO_SERVO1  = 2
GPIO_SERVO2  = 3


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(GPIO_LED_GREEN, GPIO.OUT)
GPIO.setup(GPIO_LED_RED, GPIO.OUT)
GPIO.setup(GPIO_LED_YELLOW, GPIO.OUT)
GPIO.setup(GPIO_LED_BLUE, GPIO.OUT)
GPIO.setup(GPIO_SERVO1, GPIO.OUT)
GPIO.setup(GPIO_SERVO2, GPIO.OUT)


def updateServo(pwm, angle):
    duty = float(angle) / 10.0 + 2.5
    pwm.ChangeDutyCycle(duty+SERVO_ERR)

#Convirte as coordenadas x e y en un angulo.
#Os dous cuadrantes inferiores devolven o mesmo angulo que os superiores.
def angleFromCoords(x,y):
    angle = 0.0
    if x==0.0 and y==0.0:
        angle = 90.0
    elif x>=0.0 and y>=0.0:
        # first quadrant
        angle = math.degrees(math.atan(y/x)) if x!=0.0 else 90.0
    elif x<0.0 and y>=0.0:
        # second quadrant
        angle = math.degrees(math.atan(y/x))
        angle += 180.0
    elif x<0.0 and y<0.0:
        # third quadrant
        y = y * -1
        angle = math.degrees(math.atan(y/x))
        angle += 180.0
    elif x>=0.0 and y<0.0:
        # third quadrant
        y = y * -1
        angle = math.degrees(math.atan(y/x)) if x!=0.0 else 90.0
    return angle

if __name__ == '__main__':
    joy = xbox.Joystick()
    pwm1 = GPIO.PWM(GPIO_SERVO1, 100)
    pwm2 = GPIO.PWM(GPIO_SERVO2, 100)
    pwm1.start(5)
    pwm2.start(5)

    while not joy.Back():

        try:

            # LEDs
            # Interpretamos o estado dos botons do mando da xbox.Joystick
            led_state_green  = GPIO.HIGH if joy.A() else GPIO.LOW
            led_state_red    = GPIO.HIGH if joy.B() else GPIO.LOW
            led_state_yellow = GPIO.HIGH if joy.Y() else GPIO.LOW
            led_state_blue   = GPIO.HIGH if joy.X() else GPIO.LOW

            # Aplicamos o estado do boton a un output correspondente.
            GPIO.output(GPIO_LED_GREEN, led_state_green)
            GPIO.output(GPIO_LED_RED, led_state_red)
            GPIO.output(GPIO_LED_YELLOW, led_state_yellow)
            GPIO.output(GPIO_LED_BLUE, led_state_blue)

            # Servo
            x1, y1 = joy.leftStick()
            x2, y2 = joy.rightStick()

            angle1 = angleFromCoords(x1,y1)
            angle2 = angleFromCoords(x2,y2)

            updateServo(pwm1, angle1)
            updateServo(pwm2, angle2)

        except KeyboardInterrupt:
            break


    updateServo(pwm1, 90)
    updateServo(pwm2, 90)
    time.sleep(.5)
    joy.close()
    pwm1.stop()
    pwm2.stop()
