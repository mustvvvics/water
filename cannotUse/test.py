#!/usr/bin/env python
import RPi.GPIO as GPIO
import time

RelayPin = 38   # pin11
GPIO.setmode(GPIO.BOARD)       # Numbers GPIOs by physical location
GPIO.setup(RelayPin, GPIO.OUT)
GPIO.setwarnings(False)
while(1):
    GPIO.output(RelayPin, GPIO.HIGH)
    print("ok")