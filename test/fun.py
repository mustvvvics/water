
import RPi.GPIO as GPIO         # 引入GPIO模块
import time,threading                    # 引入time模块
from matplotlib import pyplot as plt
import numpy as np
from clear_screen import clear
# from scipy.interpolate import make_interp_spline
file = "/dev/hidraw0"

funFreq = 10
funSpeed = 1.0
temperature = 0

ENB = 11                                        # site GPIO35 link ENB
IN3 = 29                                        # site GPIO31 link IN3
IN4 = 13                                     # site GPIO15 link IN4

# def pltReduceTemperature(x,y):
#     xarray = np.array(x)
#     yarray = np.array(y)
#     x_smooth = np.linspace(xarray.min(), xarray.max(), xarray.max())
#     y_smooth = make_interp_spline(xarray, yarray)(x_smooth)
#     plt.plot(x_smooth, y_smooth)
#     plt.xlim(0,20000) #x坐标轴范围-10~10
#     plt.ylim(0,700)
#     plt.grid()#网格线显示

# def pltControlReduceTemperature(x,y):
#     xarray = np.array(x)
#     yarray = np.array(y)
#     x_smooth = np.linspace(xarray.min(), xarray.max(), xarray.max())
#     y_smooth = make_interp_spline(xarray, yarray)(x_smooth)
#     plt.plot(x_smooth, y_smooth)
#     plt.xlim(-10,2000) #x坐标轴范围-10~10
#     plt.ylim(0,50)
#     plt.grid()#网格线显示

def destroy():
    GPIO.output(ENB, False) 
    GPIO.output(IN3, False)           # 将IN3对应的GPIO引脚设置为输出模式
    GPIO.output(IN4, False)           # 将IN4对应的GPIO引脚设置为输出模式
    GPIO.cleanup()                  # 清理释放GPIO资源，将GPIO复位

def funGpioIni():
    GPIO.setmode(GPIO.BOARD)            # 使用BOARD编号方式
    GPIO.setup(ENB, GPIO.OUT)           # 将ENB对应的GPIO引脚设置为输出模式
    GPIO.setup(IN3, GPIO.OUT)           # 将IN3对应的GPIO引脚设置为输出模式
    GPIO.setup(IN4, GPIO.OUT)           # 将IN4对应的GPIO引脚设置为输出模式

def funWorking():#
    GPIO.output(IN3, False)         # 将IN3设置为0
    GPIO.output(IN4, True)          # 将IN4设置为1

Sv = 250

Pv = 350

Kp = 1
T = 500
Ti = 20
Td = 0
pwmcycle = 200
OUT0 = 0
Ek_1 = 0
SEK = 0


SEk = 0

flag = 1
xlist = []
ylist = []
changeylist = []
i = 0
y = 0
xmax = 20000

def controlTemperature():
    global temperature
    global errorTemperature
    # relaySetup()
    while True:
        # Get Temperature
        fp = open(file,'rb')            
        temperature = fp.read(4)
        temperature = temperature[2:]
        temperature = int.from_bytes(temperature, byteorder="big") 
        # temperature /= 10               # e.g 301°C to 30.1°C
                                        #需要提前0.5°C
        # errorTemperature = targetTemperature - temperature 

if __name__ == '__main__':
    t1 = threading.Thread(target = controlTemperature)

    t1.start()

    try :
        funGpioIni()                           # 初始化
        pwmfun = GPIO.PWM(ENB, funFreq)           # 设置向ENB输入PWM脉冲信号，频率为freq并创建PWM对象
        pwmfun.start(funSpeed)                    # 以speed的初始占空比开始向ENB输入PWM脉冲信号

        while(True):
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
            if y == 300: #100 = 300ms# 10000 cost 33s   // each 0.0033s 
                y = 0 
                Pv = temperature
            ylist.append((-out + 500))  
            yappend = float(int(((-out + 500)/ 10) - 20))
            
            # 
            if yappend > 30.0:
                yappend = 30.0
            if yappend < 0.0:
                yappend = 0.0
            clear()
            print("yappend",yappend) 
            print("temperature",temperature) 
            pwmfun.ChangeDutyCycle(yappend)
            changeylist.append(yappend) 
            if temperature == Sv:
                pwmfun.stop() 
                # end = time.time()
                # print("time",end - start)
                # plt.show()
                flag = 0
                Ek = 0
                Ek_1 = 0
                Pout = 0
                SEk =0
                delEk = 0
                Iout = 0
                Dout = 0
                # print(i)
                i = 0
                print(len(xlist),len(ylist))
                # pltReduceTemperature(xlist,ylist)
            

    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
        print("Keyboard interrupt")
    except:
        print("some error") 
        raise
    finally:
        print("clean up") 
        pwm.stop()  
        destroy() 
