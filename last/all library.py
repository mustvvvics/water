# -*- coding: utf-8 -*-
"""
Created on Tue Apr 20 20:22:49 2021

@author: Mustvvvics
"""
import time,threading
from queue import Queue                         # q = Queue()
import cv2
from clear_screen import clear
import RPi.GPIO as GPIO         

# target#################################################################
targetHeight = 9
targetTemperature = 30

# Initial Value##########################################################
height = 0
temperature = 0
errorHeight = 0
errorTemperature = 0

# Initial Temperature####################################################
file = "/dev/hidraw0"
RelayPin = 38                                   # Relay Control

# Initial Liquid Level###################################################
RealyHighMax = 13
CameraHighMax = 364                             # Height mapping

ENA = 35                                        # site GPIO35 link ENA
IN1 = 31                                        # site GPIO31 link IN1
IN2 = 15                                        # site GPIO15 link IN2

freq = 500                                      # PWM frequency
speed = 10                                      # PWM Initialising speed
# Initial Camera Value###################################################
CV_CAP_PROP_FRAME_WIDTH = 3
CV_CAP_PROP_FRAME_HEIGHT = 4
CV_CAP_PROP_FPS = 5
CV_CAP_PROP_FOURCC = 6

name = 0
cap = cv2.VideoCapture(name)                    # Turn on the built-in camera

cap.set(CV_CAP_PROP_FPS, 1)

frameWidth = 640
frameHeight = 480

cap.set(cv2.CAP_PROP_FRAME_WIDTH, frameWidth)   # Setup form 1920 * 1080 
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, frameHeight)

ratioWindowsHeight = 1                          # Form transformation
ratioWindowsWidth = 0.6
windowsWidth = int(frameWidth * ( 0.5 - ratioWindowsWidth / 2 )), int(frameWidth * ( 0.5 + ratioWindowsWidth / 2 ))
windowsHeight = int(frameHeight * ( 0.5 - ratioWindowsHeight / 2 )), int(frameHeight * ( 0.5 + ratioWindowsHeight / 2 ))

# Flag###################################################################
flagWorking = True

# Gpio Destroy###########################################################
def gpioDestroy():
        GPIO.output(ENA, False) 
        GPIO.output(IN1, False)         
        GPIO.output(IN1, False)         
        GPIO.output(RelayPin, False)
        GPIO.cleanup()                          # clean GPIO

# Water Function#########################################################
def waterGpioIni():
        GPIO.setmode(GPIO.BOARD)                # 使用BOARD编号方式
        GPIO.setup(ENA, GPIO.OUT)               # Set the GPIO pin corresponding to ENA to output mode
        GPIO.setup(IN1, GPIO.OUT)               # Set the GPIO pin corresponding to IN1 to output mode
        GPIO.setup(IN2, GPIO.OUT)               # Set the GPIO pin corresponding to IN2 to output mode

def pumpWater():                                # water in
        GPIO.output(IN1, False)                 # Set IN1 to 0
        GPIO.output(IN2, True)                  # Set IN2 to 1

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
        GPIO.setmode(GPIO.BOARD)                # Numbers GPIOs by physical location
        GPIO.setup(RelayPin, GPIO.OUT)
        GPIO.output(RelayPin, GPIO.LOW)

# Threading##############################################################
def controlHeight():
        global errorHeight

        waterGpioIni()                           # 初始化
        pwm = GPIO.PWM(ENA, freq)           # 设置向ENA输入PWM脉冲信号，频率为freq并创建PWM对象
        pwm.start(speed)                    # 以speed的初始占空比开始向ENA输入PWM脉冲信号
        waterFlag = 1
        waterDeath = 0.05
        while flagWorking:
                
                # print("errorHeight",errorHeight)
                # time.sleep(0.05)
                if errorHeight >= waterDeath :
                        pumpWater()
                        pwm.ChangeDutyCycle(100)
                elif errorHeight <= -waterDeath :
                        releaseWater()
                        pwm.ChangeDutyCycle(100)
                elif abs(errorHeight) < waterDeath :
                        # waterFlag = 0
                        pwm.ChangeDutyCycle(0)

def getTemperature():
        global temperature
        global errorTemperature
        relaySetup()
        while flagWorking:
                
                fp = open(file,'rb')

                temperature = fp.read(4)
                temperature = temperature[2:]
                temperature = int.from_bytes(temperature, byteorder="big") #311
                temperature /= 10 

                errorTemperature = targetTemperature - temperature #需要提前0.5°
                if errorTemperature > 0.2:      # Working
                        GPIO.output(RelayPin, GPIO.LOW)
                if errorTemperature <= 0.2:     # Close
                        GPIO.output(RelayPin, GPIO.HIGH)

if __name__ == '__main__':
        t1 = threading.Thread(target = getTemperature)
        t2 = threading.Thread(target = controlHeight)
        # t4 = threading.Thread(target = controlTemperature,args=(targetTemperature,))
                
        t1.start()
        t2.start()
        # t4.start()

        try: 
                while(1):
                        # start = time.time()

                        ret,img = cap.read() #实时读取图像
                        img = img[ windowsHeight[0] : windowsHeight[1], windowsWidth[0] : windowsWidth[1]]

                        imggray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY) # cv2.cvtColor(src, code[, dst[, dstCn]])
                        ret, thresh = cv2.threshold(imggray,50,255,0)#简单阈值 黑色识别
                        _, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)#用来绘制轮廓
                        
                        for cnt in contours:
                                if (cv2.contourArea(cnt) > 3000) and (cv2.contourArea(cnt) < 52000):
                                        # draw a rectangle around the items
                                        # clear() #清屏 
                                        print(cv2.contourArea(cnt))
                                        x,y,w,h = cv2.boundingRect(cnt)
                                        cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0),3)
                                        print(h)
                                        height = CalculationHigh(h)
                                        errorHeight = targetHeight - height
                        
                        # clear() #清屏      
                        print("目标液位",targetHeight,"目标温度",targetTemperature)
                        print("当前液位",height,"当前温度",temperature)
                        print("误差液位",errorHeight,"误差温度",errorTemperature)

                        cv2.imshow("-1", img)
                        
                        k = cv2.waitKey(1)
                        if (k == ord('q')):
                                break
                        elif(k == ord('s')):
                                #name = input('name:')
                                name += 1
                                filename = '/home/pi/sheji/' + str(name) + 'test' + '.jpg'
                                cv2.imwrite(filename, img)
                                # print(filename)
                                #break 
        except KeyboardInterrupt:
                print("ancled program.")
        except:
                raise
        finally:       
                flagWorking = False
                gpioDestroy()
                cv2.destroyAllWindows()