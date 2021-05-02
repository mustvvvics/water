# -*- coding: utf-8 -*-
"""
Created on Tue Apr 20 20:22:49 2021

@author: Mustvvvics
"""
import time,threading
from queue import Queue
import cv2
from clear_screen import clear
import RPi.GPIO as GPIO         
#target#################################################################
targetHeight = 9
targetTemperature = 30
########################################################################

#Initial value##########################################################
height = 0
temperature = 0
errorHeight = 0
errorTemperature = 0
########################################################################
file = "/dev/hidraw0"
# q = Queue()
########################################################################
CV_CAP_PROP_FRAME_WIDTH = 3
CV_CAP_PROP_FRAME_HEIGHT = 4
CV_CAP_PROP_FPS = 5
CV_CAP_PROP_FOURCC = 6

name = 0
cap = cv2.VideoCapture(name) #打开内置摄像头

cap.set(CV_CAP_PROP_FPS, 1)

frameWidth = 640
frameHeight = 480

cap.set(cv2.CAP_PROP_FRAME_WIDTH, frameWidth) #设置窗体 1920 * 1080 
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, frameHeight)

#窗体变换
ratioWindowsHeight = 1
ratioWindowsWidth = 0.6
windowsWidth = int(frameWidth * ( 0.5 - ratioWindowsWidth / 2 )), int(frameWidth * ( 0.5 + ratioWindowsWidth / 2 ))
windowsHeight = int(frameHeight * ( 0.5 - ratioWindowsHeight / 2 )), int(frameHeight * ( 0.5 + ratioWindowsHeight / 2 ))
########################################################################

flagWorking = True
########################################################################
ENA = 35                        # 设置GPIO35连接ENA
IN1 = 31                       # 设置GPIO31连接IN1
IN2 = 15                         # 设置GPIO15连接IN2
RelayPin = 38   # pin11
freq = 500
speed = 10
#water########################################################################
def destroy():
        GPIO.output(ENA, False) 
        # time.sleep(0.5)   
        GPIO.cleanup()                  # 清理释放GPIO资源，将GPIO复位

def waterGpioIni():
        GPIO.setmode(GPIO.BOARD)            # 使用BOARD编号方式
        GPIO.setup(ENA, GPIO.OUT)           # 将ENA对应的GPIO引脚设置为输出模式
        GPIO.setup(IN1, GPIO.OUT)           # 将IN1对应的GPIO引脚设置为输出模式
        GPIO.setup(IN2, GPIO.OUT)           # 将IN2对应的GPIO引脚设置为输出模式

def pumpWater():#water in
        # 将电机设置为正向转动 
        GPIO.output(IN1, False)         # 将IN1设置为0
        GPIO.output(IN2, True)          # 将IN2设置为1
def releaseWater():#water out
        GPIO.output(IN1, True)         
        GPIO.output(IN2, False) 

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
                
                        
########################################################################
def CalculationHigh(h):
        RealyHighMax = 13
        CameraHighMax = 364

        if h > 0 :
                high =  (RealyHighMax / CameraHighMax) * h
        else:
                high = 0
        return high

########################################################################
def setup():
        GPIO.setmode(GPIO.BOARD)       # Numbers GPIOs by physical location
        GPIO.setup(RelayPin, GPIO.OUT)
        GPIO.output(RelayPin, GPIO.LOW)

########################################################################
def getTemperature():
        global temperature
        global errorTemperature
        setup()
        while flagWorking:
                
                fp = open(file,'rb')

                temperature = fp.read(4)
                temperature = temperature[2:]
                temperature = int.from_bytes(temperature, byteorder="big") #311
                temperature /= 10 

                errorTemperature = targetTemperature - temperature #需要提前0.5°
                if errorTemperature > 0.2:
                        GPIO.output(RelayPin, GPIO.LOW)#低电平时，继电器为初始状态
                if errorTemperature <= 0.2:
                        GPIO.output(RelayPin, GPIO.HIGH)#高电平时，继电器为激活状态
                
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
                destroy()
                cv2.destroyAllWindows()