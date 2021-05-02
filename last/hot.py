import RPi.GPIO as GPIO         # 引入GPIO模块
import time                     # 引入time模块

ENA = 35                        # 设置GPIO13连接ENA
IN1 = 31                      # 设置GPIO19连接IN1
IN2 = 15                         # 设置GPIO26连接IN2

def destroy():
        GPIO.output(ENA, False) 
        time.sleep(0.5)   
        # GPIO.cleanup()                     # Release resource

if __name__ == '__main__':
        try:
            # 初始化
            GPIO.setmode(GPIO.BOARD)          # 使用BCM编号方式

            GPIO.setup(ENA, GPIO.OUT)       # 将连接ENA的GPIO引脚设置为输出模式
            GPIO.setup(IN1, GPIO.OUT)       # 将连接IN1的GPIO引脚设置为输出模式
            GPIO.setup(IN2, GPIO.OUT)       # 将连接IN2的GPIO引脚设置为输出模式

            while True:
                # 驱动电机正向旋转5秒
                GPIO.output(IN1, False)     # 将IN1设置为0
                GPIO.output(IN2, True)      # 将IN2设置为1
                GPIO.output(ENA, True)      # 将ENA设置为1，启动A通道电机
                time.sleep(2)               # 等待电机转动5秒

                # 电机停止2秒
                GPIO.output(ENA, False)     # 将ENA设置为0
                time.sleep(4)               # 等待电机停止2秒

                # # 驱动电机反向旋转5秒
                # GPIO.output(IN1, True)      # 将IN1设置为1
                # GPIO.output(IN2, False)     # 将IN2设置为0
                # GPIO.output(ENA, True)      # 将ENA设置为1，启动A通道电机
                # time.sleep(5)               # 等待电机转动5秒

                # # 电机停止2秒
                # GPIO.output(ENA, False)     # 将ENA设置为0
                # time.sleep(2)               # 等待电机停止2秒
        except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
                # GPIO.output(RelayPin, GPIO.LOW)
                # pwm.stop()                      # 停止PWM
                destroy()
                GPIO.cleanup()                  # 清理释放GPIO资源，将GPIO复位