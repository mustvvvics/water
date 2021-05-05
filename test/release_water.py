import RPi.GPIO as GPIO         # 引入GPIO模块
import time                     # 引入time模块

ENA = 35                        # 设置GPIO35连接ENA
IN1 = 31                       # 设置GPIO31连接IN1
IN2 = 15                         # 设置GPIO15连接IN2

freq = 500
speed = 10
dutyRatio = 0
errorHeight = 5

def destroy():
    GPIO.output(ENA, False) 
    # time.sleep(0.5)   
    GPIO.cleanup()                  # 清理释放GPIO资源，将GPIO复位

def gpioIni():
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

# def changePwm(speed):
#         for speed in range(99, 101, 1):
#                 pwm.ChangeDutyCycle(speed)  # 通过改变PWM占空比，让电机转速不断加快
#                 print("speed",speed)
#                 time.sleep(1)

# def pidDutyRatio(errorHeight):


if __name__ == '__main__':
# def doWaterControl(errorHeight):
    try :
        gpioIni()                           # 初始化
        pwm = GPIO.PWM(ENA, freq)           # 设置向ENA输入PWM脉冲信号，频率为freq并创建PWM对象
        pwm.start(speed)                    # 以speed的初始占空比开始向ENA输入PWM脉冲信号
        waterFlag = 1

        while(True):
            releaseWater()
            # pumpWater()
            # pwm.ChangeDutyCycle(dutyRatio)
            pwm.ChangeDutyCycle(100)


    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
        print("Keyboard interrupt")
    except:
        print("some error") 
    finally:
        print("clean up") 
        pwm.stop()                      # 停止PWM
        destroy() # cleanup all GPIO 

                