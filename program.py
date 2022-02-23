import RPi.GPIO as GPIO
from time import sleep
import time
import threading

detected = False

def detect_motion():
    sensor = 16
    buzzer = 18
    global detected 

    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(sensor,GPIO.IN)
    GPIO.setup(buzzer,GPIO.OUT)

    try: 
        while True:
            if GPIO.input(sensor):
                detected = False
                GPIO.output(buzzer,False)
            else:
                GPIO.output(buzzer,True)
                detected = True
                print ("Train passing by!!!")
                time.sleep(3)
            time.sleep(0.2)
    except KeyboardInterrupt:
        GPIO.cleanup()

def blink():
    red = 15
    amber = 13
    green = 11
    buzzer = 37

    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(red,GPIO.OUT)
    GPIO.setup(amber,GPIO.OUT)
    GPIO.setup(green,GPIO.OUT)
    GPIO.setup(buzzer,GPIO.OUT)

    current_value=False
    while True:
        if detected:
            GPIO.output(red, not current_value)
            GPIO.output(buzzer,not current_value);  
            GPIO.output(amber, current_value)
            GPIO.output(green, False)  
            current_value=not current_value
        else:
            GPIO.output(red, False)
            GPIO.output(amber, False)      
            GPIO.output(green, True)  
            GPIO.output(buzzer,False);  
            # Reset to always start with red
            current_value=False
        sleep(0.5)

thr = threading.Thread(target=blink, args=(), kwargs={})
thr.start() 

detect_motion()