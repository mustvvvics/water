import RPi.GPIO as GPIO         # 引入GPIO模块
import time                     # 引入time模块


ENA = 35                                        # site GPIO35 link ENA
IN1 = 31                                        # site GPIO31 link IN1
IN2 = 15                                        # site GPIO15 link IN2

freq = 10
speed = 1
# dutyRatio = 0
# errorHeight = 5

ENB = 11                                        # site GPIO35 link ENB
IN3 = 29                                        # site GPIO31 link IN3
IN4 = 7                                        # site GPIO15 link IN4

def destroy():
    GPIO.output(ENB, False) 
    GPIO.output(IN3, False)           # 将IN3对应的GPIO引脚设置为输出模式
    GPIO.output(IN4, False)           # 将IN4对应的GPIO引脚设置为输出模式
    # time.sleep(0.5)   
    #GPIO.cleanup()                  # 清理释放GPIO资源，将GPIO复位

def gpioIni():
    GPIO.setmode(GPIO.BOARD)            # 使用BOARD编号方式
    GPIO.setup(ENB, GPIO.OUT)           # 将ENB对应的GPIO引脚设置为输出模式
    GPIO.setup(IN3, GPIO.OUT)           # 将IN3对应的GPIO引脚设置为输出模式
    GPIO.setup(IN4, GPIO.OUT)           # 将IN4对应的GPIO引脚设置为输出模式


def pumpWater():#water in
    # 将电机设置为正向转动 
    GPIO.output(IN3, False)         # 将IN3设置为0
    GPIO.output(IN4, True)          # 将IN4设置为1

def releaseWater():#water out
    GPIO.output(IN3, True)         
    GPIO.output(IN4, False)       

def adestroy():
    GPIO.output(ENA, False) 
    GPIO.output(IN1, False)           # 将IN1对应的GPIO引脚设置为输出模式
    GPIO.output(IN2, False)           # 将IN2对应的GPIO引脚设置为输出模式
    # time.sleep(0.5)   
    GPIO.cleanup()                  # 清理释放GPIO资源，将GPIO复位

def agpioIni():
    GPIO.setmode(GPIO.BOARD)            # 使用BOARD编号方式
    GPIO.setup(ENA, GPIO.OUT)           # 将ENA对应的GPIO引脚设置为输出模式
    GPIO.setup(IN1, GPIO.OUT)           # 将IN1对应的GPIO引脚设置为输出模式
    GPIO.setup(IN2, GPIO.OUT)           # 将IN2对应的GPIO引脚设置为输出模式


def apumpWater():#water in
    # 将电机设置为正向转动 
    GPIO.output(IN1, False)         # 将IN1设置为0
    GPIO.output(IN2, True)          # 将IN2设置为1

def areleaseWater():#water out
    GPIO.output(IN1, True)         
    GPIO.output(IN2, False)       


if __name__ == '__main__':
# def doWaterControl(errorHeight):
    try :
        gpioIni()                           # 初始化
        agpioIni()
        pwm = GPIO.PWM(ENB, freq)           # 设置向ENB输入PWM脉冲信号，频率为freq并创建PWM对象
        pwma = GPIO.PWM(ENA, freq)           # 设置向ENB输入PWM脉冲信号，频率为freq并创建PWM对象

        pwm.start(30)                    # 以speed的初始占空比开始向ENB输入PWM脉冲信号
        pwma.start(30)                    # 以speed的初始占空比开始向ENB输入PWM脉冲信号

        while(True):
            # releaseWater()
            # areleaseWater()
            pumpWater()
            apumpWater()

            # for c in range(100):
            # # pwm.ChangeDutyCycle(dutyRatio)
            #         pwm.ChangeDutyCycle(c)
            #         pwma.ChangeDutyCycle(c)
            #         print(c)
            #         time.sleep(0.2)
            # # pwm.ChangeDutyCycle(40)
    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
        print("Keyboard interrupt")
    except:
        print("some error") 
    finally:
        print("clean up") 
        pwm.stop()                      # 停止PWM
        destroy() # cleanup all GPIO 
        adestroy()

                