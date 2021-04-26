import time,threading
from camera import camera

targetHeight = 300
targetTemperature = 90
height = 0
temperature = 0
errorHeight = 0
errorTemperature = 0
########################################################################
def getHeight():
        global height
        height = 100
        # camera.cameraInitialization()
        while(1):
            ret,img = cap.read() #实时读取图像
            # print(f"img shape {img.shape}")
            # img h*w*3

            img = img[ windowsHeight[0] : windowsHeight[1], windowsWidth[0] : windowsWidth[1]]
            print(img.shape)

            # print("img shape",img.shape)
            # print("img",img)
            start1 = time.time()
            camera.ShowContours(img)
            end1 = time.time()
            print("ShowContours time",end1-start1)

            k = cv2.waitKey(5)
            if (k == ord('q')):
                break
            elif(k == ord('s')):
                    #name = input('name:')
                    name += 1
                    filename = '/home/pi/sheji/' + str(name) + 'test' + '.jpg'
                    cv2.imwrite(filename, img)
                    print(filename)
                    #break 
        cap.release()
        cv2.destroyAllWindows()

def getTemperature():
        global temperature
        temperature = 30

def controlHeight(targetHeight):
        global errorHeight
        errorHeight = targetHeight -height

def controlTemperature(targetTempearture):
        global errorTemperature
        errorTemperature = targetTemperature - temperature

t1 = threading.Thread(target = getHeight)
t2 = threading.Thread(target = getTemperature)
t3 = threading.Thread(target = controlHeight,args=(targetHeight,))
t4 = threading.Thread(target = controlTemperature,args=(targetTemperature,))

t1.start()
t2.start()
t3.start()
t4.start()

t1.join()
t2.join()
t3.join()
t4.join()

print(height,temperature)
print(errorHeight,errorTemperature)