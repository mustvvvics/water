#!/usr/bin/env python
import RPi.GPIO as GPIO
import time

RelayPin = 11   # pin11

def setup():
    GPIO.setmode(GPIO.BOARD)       # Numbers GPIOs by physical location
    GPIO.setup(RelayPin, GPIO.OUT)
    GPIO.output(RelayPin, GPIO.LOW)

def loop():
    while True:
        print ('常闭触点通电...')
        GPIO.output(RelayPin, GPIO.LOW)#低电平时，继电器为初始状态
        time.sleep(2)                #常闭触点通电，绿灯亮
        print ('常开触点通电...') 
        GPIO.output(RelayPin, GPIO.HIGH)#高电平时，继电器为激活状态
        time.sleep(2)                 #常开触点通电，红灯亮

def destroy():
    GPIO.output(RelayPin, GPIO.LOW)
    time.sleep(0.5)   
    # GPIO.cleanup()                     # Release resource

if __name__ == '__main__':     # Program start from here
    setup()
    try:
        loop()
        # GPIO.output(RelayPin, GPIO.LOW)
    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
        # GPIO.output(RelayPin, GPIO.LOW)
        destroy()