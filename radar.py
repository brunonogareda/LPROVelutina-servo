import RPi.GPIO as GPIO
import time

SERVO_ERR = 3

# Servo position control func
def update(angle):
    duty = float(angle) / 10 + 2.5
    pwm.ChangeDutyCycle(duty+SERVO_ERR)

#IO pin numbers
TRIG = 11
ECHO = 13
SERVO = 3

#Setup IO ports
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

GPIO.setup(SERVO, GPIO.OUT)

pwm = GPIO.PWM(SERVO, 100)
pwm.start(5)

GPIO.output(TRIG, False)

#Initialise variables
direction = True
angle = 0
pos = 0
pos_prev = 17
pulse_start = 0
pulse_end = 0

b = [ 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0 ]
c = [ 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0 ]

#Main loop
while True :
    #Send trigger (start) pulse to US sensor
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    #Wait until RX signal 0 or max delay
    timeout = 0
    while (GPIO.input(ECHO)==GPIO.LOW) and (timeout < 50):
        timeout = timeout + 1
        pulse_start = time.time()

    #Wait for RX signal
    while GPIO.input(ECHO)==GPIO.HIGH:
        pulse_end = time.time()

    #Calculate time of flight
    pulse_duration = pulse_end - pulse_start

    #convert time to distance
    distance = pulse_duration * 17150
    distance = round(distance, 2)

    #Trap if no pulse recieved
    if distance < 0:
        distance = 0

    distance = distance * 10

    #Set max distance for display
    if distance > 600:
        distance = 600

    print "Distance: ", distance,"mm", "Angle: ", pos

    #Move sensor head
    update(angle)
    time.sleep(0.5)

    #update log file
    file = open('plot_1.dat', 'w')
    outputString = "\n"

    #this array contains a single value i.e. scan line on plot
    c[pos] = 600
    c[pos_prev] = 0

    #update distance string with new value
    for i in range(0,18):
        if pos == i:
            b[i] = distance

        outputString = outputString + str(i*10) + "\t" + str(b[i]) + "\t" + str(c[i]) + "\n"

    #write data to file
    file.write(outputString)
    file.close
    #update scan direction and position
    pos_prev = pos

    if direction:
        angle = angle + 10
        pos = pos + 1
    else:
        angle = angle - 10
        pos = pos - 1

    if angle > 180:
        direction = False
        angle = 170
        pos = 17

    if angle < 0:
        direction = True
        angle = 10
        pos = 1
