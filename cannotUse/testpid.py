import pid_control

def print_obj(obj):
    "打印对象的所有属性"
    print(obj.__dict__)

if __name__ == "__main__":
        try:
            while(1):
                pid = pid_control.PID_Controller(50, 20)
                print_obj(pid)
        except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
                # GPIO.output(RelayPin, GPIO.LOW)
                # break
                print("end")