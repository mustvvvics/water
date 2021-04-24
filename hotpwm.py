import RPi.GPIO as GPIO         # 引入GPIO模块
import time                     # 引入time模块

ENA = 13                        # 设置GPIO13连接ENA
IN1 = 31                       # 设置GPIO19连接IN1
IN2 = 32                         # 设置GPIO26连接IN2

def destroy():
    GPIO.output(ENA, False) 
    time.sleep(0.5)   
    # GPIO.cleanup()                     # Release resource

if __name__ == '__main__':
    try:
        # 初始化
        GPIO.setmode(GPIO.BOARD)              # 使用BCM编号方式
        GPIO.setup(ENA, GPIO.OUT)           # 将ENA对应的GPIO引脚设置为输出模式
        GPIO.setup(IN1, GPIO.OUT)           # 将IN1对应的GPIO引脚设置为输出模式
        GPIO.setup(IN2, GPIO.OUT)           # 将IN2对应的GPIO引脚设置为输出模式

        freq = 500
        speed = 10
        pwm = GPIO.PWM(ENA, freq)           # 设置向ENA输入PWM脉冲信号，频率为freq并创建PWM对象

        pwm.start(speed)                    # 以speed的初始占空比开始向ENA输入PWM脉冲信号

        while True:
            # 将电机设置为正向转动
            GPIO.output(IN1, False)         # 将IN1设置为0
            GPIO.output(IN2, True)          # 将IN2设置为1
            print("ok1")
            # 通过改变PWM占空比，让电机转速不断加快
            for speed in range(10, 100, 5):
                pwm.ChangeDutyCycle(speed)  # 改变PWM占空比
                print("ok2")
                print(speed)
                time.sleep(1)
                if speed == 100:
                    pwm.stop()                      # 停止PWM
                    destroy()
                    GPIO.cleanup()                  # 清理释放GPIO资源，将GPIO复位
                    break

            # # 将电机设置为反向转动
            # GPIO.output(IN1, True)          # 将IN1设置为1
            # GPIO.output(IN2, False)         # 将IN2设置为0

            # # 通过改变PWM占空比，让电机转速不断加快
            # for speed in range(0, 100, 5):
            #     pwm.ChangeDutyCycle(speed)  # 改变PWM占空比
            #     time.sleep(1)
    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
            # GPIO.output(RelayPin, GPIO.LOW)
            pwm.stop()                      # 停止PWM
            destroy()
            GPIO.cleanup()                  # 清理释放GPIO资源，将GPIO复位