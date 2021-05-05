# -*- coding: utf-8 -*-
"""
Created on Tue Apr 20 20:22:49 2021

@author: Mustvvvics
"""
import time,threading
from multiprocessing import Process, Value
from time import sleep
from queue import Queue                               
import cv2
from clear_screen import clear
import RPi.GPIO as GPIO         
import numpy as np

import socket
from tcpclient import sendData
from tcpcommon import device, bufferSize, printT, getJson
import requests as r

# target#################################################################
targetHeight = Value('f', 9)
targetTemperature = Value('f', 30) 

# Initial fun pid ########################################################
Sv = targetTemperature.value * 10
Pv = 350

Kp = 1
T = 500
Ti = 20
Td = 0
pwmcycle = 200
OUT0 = 0
Ek_1 = 0
SEk = 0
xlist = []
ylist = []
changeylist = []
i = 0
y = 0

# Initial Value##########################################################
height = Value('f', 0)
temperature = Value('f', 0)
errorHeight = Value('f', 0)
errorTemperature = Value('f', 0)

# Initial Temperature####################################################
file = "/dev/hidraw0"
RelayPin = 38                                   # Relay Control

# Initial fun############################################################
funFreq = 10
funSpeed = 30
ENB = 11                                        # site GPIO11 link ENB
IN3 = 29                                        # site GPIO29 link IN3
IN4 = 13                                        # site GPIO13 link IN4

# Initial Liquid Level###################################################
RealyHighMax = 13
CameraHighMax = 364                             # Height mapping

ENA = 35                                        # site GPIO35 link ENA
IN1 = 31                                        # site GPIO31 link IN1
IN2 = 15                                        # site GPIO15 link IN2

freq = 500                                      # PWM frequency
speed = 10                                      # PWM Initialising speed

# Flag###################################################################
flagWorking = True
temperatureFlag = 0                             # 0:heating 1:drop temperature

# Gpio Destroy###########################################################
def gpioDestroy():
    GPIO.output(ENA, False) 
    GPIO.output(IN1, False)         
    GPIO.output(IN1, False)         
    GPIO.output(RelayPin, False)
    GPIO.output(ENB, False) 
    GPIO.output(IN3, False)           
    GPIO.output(IN4, False)          
    GPIO.cleanup()                              # clean GPIO

# Water Function#########################################################
def waterGpioIni():
    GPIO.setmode(GPIO.BOARD)                    # use BOARD
    GPIO.setup(ENA, GPIO.OUT)                   # Set the GPIO pin corresponding to ENA to output mode
    GPIO.setup(IN1, GPIO.OUT)                   # Set the GPIO pin corresponding to IN1 to output mode
    GPIO.setup(IN2, GPIO.OUT)                   # Set the GPIO pin corresponding to IN2 to output mode

def pumpWater():                                # water in
    GPIO.output(IN1, False)                     # Set IN1 to 0
    GPIO.output(IN2, True)                      # Set IN2 to 1

def releaseWater():                             # water out
    GPIO.output(IN1, True)         
    GPIO.output(IN2, False) 

def CalculationHigh(h):                         # Calculate the water level
    if h > 0 :
        high =  (RealyHighMax / CameraHighMax) * h
    else:
        high = 0
    return high

# relay Function#########################################################
def relaySetup():
    GPIO.setmode(GPIO.BOARD)                    # Numbers GPIOs by physical location
    GPIO.setup(RelayPin, GPIO.OUT)
    GPIO.output(RelayPin, GPIO.HIGH)

# fun Function###########################################################
def funGpioIni():
    # GPIO.setmode(GPIO.BOARD)                  #have set in relay
    GPIO.setup(ENB, GPIO.OUT)               
    GPIO.setup(IN3, GPIO.OUT)               
    GPIO.setup(IN4, GPIO.OUT)                

def funWorking():#
    GPIO.output(IN3, False)                 
    GPIO.output(IN4, True)                  

# Threading##############################################################
def controlHeight():
    global errorHeight

    waterGpioIni()                        
    pwm = GPIO.PWM(ENA, freq)                   # Set the input PWM pulse signal to ENA, the frequency is freq and create a PWM object
    pwm.start(speed)                            # Start inputting PWM pulse signal to ENA with the initial duty ratio of speed
    waterDeath = 0.08

    while flagWorking:
        if errorHeight.value >= waterDeath :
            pumpWater()
            pwm.ChangeDutyCycle(100)
        elif errorHeight.value <= -waterDeath :
            releaseWater()
            pwm.ChangeDutyCycle(100)
        elif abs(errorHeight.value) < waterDeath :
            pwm.ChangeDutyCycle(0)

def controlTemperature():
    global temperature
    global errorTemperature
    global i,y,Sv,Pv,Kp,T,Ti,Td,pwmcycle,OUT0,Ek_1,SEk,xlist,ylist,changeylist
    relaySetup()
    funGpioIni()                            
    pwmfun = GPIO.PWM(ENB, funFreq)         
                     
    while flagWorking:
        # Get Temperature
        fp = open(file,'rb')            
        temperature.value = int.from_bytes(fp.read(4)[2:], byteorder='big')
        funTemperature = temperature.value
        temperature.value /= 10                 # e.g 301°C to 30.1°C
        errorTemperature.value = targetTemperature.value - temperature.value
        # Heating to 30 needs to be advanced 0.5°C, heating to 35 needs to be advanced 0°C 
        advancedTemperature = 0.5

        if errorTemperature.value >= 0:
            temperatureFlag = 0
        elif errorTemperature.value < 0:
            temperatureFlag = 1

        if temperatureFlag == 0:                # Heating
            if (errorTemperature.value - advancedTemperature) > 0.2:      # Working
                GPIO.output(RelayPin, GPIO.LOW)
            if (errorTemperature.value - advancedTemperature) <= 0.2:     # Close
                GPIO.output(RelayPin, GPIO.HIGH)
        elif temperatureFlag == 1:
            pwmfun.start(funSpeed) 
            funWorking()

            i += 1
            xlist.append(i)
            y += 1
            Ek = Sv - Pv
            Pout = Ek * Kp/10
            SEk += Ek
            delEk = Ek - Ek_1
            Iout = SEk / (Ti*10)
            Dout = Td * delEk/10
            out = Pout + Iout + Dout + OUT0
            Ek_1 = Ek
            if y == 100:                        # sampling time：100 = 300ms  10000 cost 33s    
                y = 0 
                Pv = funTemperature
            ylist.append((-out + 500))  
            yappend = int(((-out + 500)/ 10) - 20)
            
            if yappend > 30:
                yappend = 30
            if yappend < 0:
                yappend = 0
            # clear()
            # print("yappend",yappend) 
            # print("temperature",funTemperature) 
            pwmfun.ChangeDutyCycle(yappend)     
            changeylist.append(yappend) 
            if temperature.value == Sv:
                # plt.show()
                flag = 0
                Ek = 0
                Ek_1 = 0
                Pout = 0
                SEk =0
                delEk = 0
                Iout = 0
                Dout = 0
                i = 0

# Process################################################################
def cameraProcess(height, errorHeight, targetHeight):
    # Initial Camera Value
    CV_CAP_PROP_FRAME_WIDTH = 3
    CV_CAP_PROP_FRAME_HEIGHT = 4
    CV_CAP_PROP_FPS = 5
    CV_CAP_PROP_FOURCC = 6

    name = 0
    cap = cv2.VideoCapture(name)                    # Turn on the built-in camera

    cap.set(CV_CAP_PROP_FPS, 1)

    frameWidth = 640
    frameHeight = 480

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, frameWidth)   
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, frameHeight)

    ratioWindowsHeight = 1                          # Form transformation
    ratioWindowsWidth = 0.6
    windowsWidth = int(frameWidth * ( 0.5 - ratioWindowsWidth / 2 )), int(frameWidth * ( 0.5 + ratioWindowsWidth / 2 ))
    windowsHeight = int(frameHeight * ( 0.5 - ratioWindowsHeight / 2 )), int(frameHeight * ( 0.5 + ratioWindowsHeight / 2 ))

    while True:
        ret,img = cap.read()                        #Read the image in real time
        img = img[ windowsHeight[0] : windowsHeight[1], windowsWidth[0] : windowsWidth[1]]

        imggray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(imggray,50,255,0)
        _, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        
        heightTemp = 0
        for cnt in contours:
            if (cv2.contourArea(cnt) > 3000) and (cv2.contourArea(cnt) < 52000):
                # draw a rectangle around the items
                clear()                             #clear 
                print(cv2.contourArea(cnt))
                x,y,w,h = cv2.boundingRect(cnt)
                cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0),3)
                print("height", h)
                heightTemp = CalculationHigh(h)
        height.value = heightTemp
        errorHeight.value = targetHeight.value - height.value

        print("目标液位",targetHeight.value,"\t目标温度",targetTemperature.value)
        print("当前液位",round(height.value, 2), "\t当前温度",round(temperature.value, 1))
        print("误差液位",round(errorHeight.value, 2),"\t误差温度",round(errorTemperature.value, 1))

        cv2.imshow("Camera", img)
        
        k = cv2.waitKey(1)
        if (k == ord('q')):
            break
        elif(k == ord('s')):                        # Take Photo
            name += 1
            filename = '/home/pi/sheji/' + str(name) + 'test' + '.jpg'
            cv2.imwrite(filename, img)
            break 
    cv2.destroyAllWindows()

# deal Tcp Fuction#######################################################
def dealTcpData(jsonData):
    global targetHeight
    global targetTemperature

    command = jsonData['data']
    print(command)
    if (command == "higher"):
        targetHeight.value += 2
    elif (command == "lower"):
        targetHeight.value -= 2
    elif (command == "hotter"):
        targetTemperature.value += 1
    elif (command == "cooler"):
        targetTemperature.value -= 1
    else:
        return "command error"
    return "con ok"

def tcpServer():
    # server main below
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serversocket:
        serversocket.bind(device['ras'])
        serversocket.settimeout(3.0)
        serversocket.listen(5)  
        # max listen num: only listen one connection to avoid data seperation
        printT(f"Listening to {device['ras']}.")
        while flagWorking:
            try:
                try:
                    clientsocket, addr = serversocket.accept()
                except socket.timeout:
                    continue
                printT(f"Client addr: {addr}")

                jsonData = getJson(clientsocket)
                reply = dealTcpData(jsonData)
                if reply is None:
                    reply = "200 ok"

                printT("Ending connection.")
                clientsocket.send(reply.encode('utf-8'))
                clientsocket.close()
                print()
                printT(f"Listening to {device['ras']}.")

            except socket.timeout:
                printT("Error: Connection timeout.")
            except KeyboardInterrupt:
                printT("Server terminated by user.")
                break

def makeUpdate():
    url = 'https://taobooooo.top/waterlu'
    # t -- temperature, l - water height, dt -- target temperature, dl -- target water height
    while flagWorking:
        time.sleep(1)
        msg = {
            'mode': 'u',
            't': round(temperature.value, 1),
            'l': round(height.value, 1),
            'dt': round(targetTemperature.value, 1),
            'dl': round(targetHeight.value, 1),
        }
        try:
            echo = r.post(url, data = msg)
        except ConnectionRefusedError:
            return 'ras error'

# Main Threading#########################################################
if __name__ == '__main__':
    t1 = threading.Thread(target = controlTemperature)
    t2 = threading.Thread(target = controlHeight)

    tServer = threading.Thread(target = tcpServer)
    tUpdate = threading.Thread(target = makeUpdate)

    pCamera = Process(target = cameraProcess, args=(height, errorHeight, targetHeight))

    t1.start()
    t2.start()

    tServer.start()
    tUpdate.start()

    pCamera.start()
    pCamera.join()

    print("clean all.")
    flagWorking = False
    gpioDestroy()
