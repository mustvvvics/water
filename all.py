import time,threading
from queue import Queue

import cv2
from clear_screen import clear

targetHeight = 10
targetTemperature = 30
height = 0
temperature = 0
errorHeight = 0
errorTemperature = 0

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

def CalculationHigh(h):
        RealyHighMax = 13
        CameraHighMax = 321

        if h > 0 :
                high =  (RealyHighMax / CameraHighMax) * h
        else:
                high = 0
        return high

def getTemperature():
        global temperature
        global errorTemperature
        while flagWorking:
                
                fp = open(file,'rb')

                temperature = fp.read(4)
                temperature = temperature[2:]
                temperature = int.from_bytes(temperature, byteorder="big") #311
                temperature /= 10 

                errorTemperature = targetTemperature - temperature
                
if __name__ == '__main__':
        t1 = threading.Thread(target = getTemperature)
        # t3 = threading.Thread(target = controlHeight,args=(targetHeight,))
        # t4 = threading.Thread(target = controlTemperature,args=(targetTemperature,))
                
        t1.start()
        # t3.start()
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
                                if (cv2.contourArea(cnt) > 3000) and (cv2.contourArea(cnt) < 50000):
                                        # draw a rectangle around the items
                                        x,y,w,h = cv2.boundingRect(cnt)
                                        cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0),3)
                                        height = CalculationHigh(h)
                                        errorHeight = targetHeight - height
                        
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

                        clear() #清屏      
                        print("目标液位",targetHeight,"目标温度",targetTemperature)
                        print("当前液位",height,"当前温度",temperature)
                        print("误差液位",errorHeight,"误差温度",errorTemperature)
        except KeyboardInterrupt:
                print("ancled program.")
        except:
                raise
        finally:       
                flagWorking = False
                cv2.destroyAllWindows()