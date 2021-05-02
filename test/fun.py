
import RPi.GPIO as GPIO         # 引入GPIO模块
import time                     # 引入time模块

funFreq = 10
funSpeed = 1


ENB = 11                                        # site GPIO35 link ENB
IN3 = 29                                        # site GPIO31 link IN3
IN4 = 13                                     # site GPIO15 link IN4

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

if __name__ == '__main__':
    try :
        funGpioIni()                           # 初始化
        pwm = GPIO.PWM(ENB, funFreq)           # 设置向ENB输入PWM脉冲信号，频率为freq并创建PWM对象
        pwm.start(funSpeed)                    # 以speed的初始占空比开始向ENB输入PWM脉冲信号

        while(True):
            funWorking()
            pwm.ChangeDutyCycle(30)
            # for c in range(30):
            #     pwm.ChangeDutyCycle(c)
            #     print(c)
            #     time.sleep(0.2)

    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
        print("Keyboard interrupt")
    except:
        print("some error") 
    finally:
        print("clean up") 
        pwm.stop()  
        destroy() 

