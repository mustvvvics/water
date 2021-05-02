import RPi.GPIO as GPIO  
import time
RelayPin = 38 

GPIO.setmode(GPIO.BOARD)       # Numbers GPIOs by physical location
GPIO.setup(RelayPin, GPIO.OUT)
# GPIO.output(RelayPin, GPIO.HIGH) 
if __name__ == '__main__':


        try: 
            while(1):
                GPIO.output(RelayPin, GPIO.LOW)
                print("OK")
                time.sleep(1)

                GPIO.output(RelayPin, GPIO.HIGH)
                print("OK2")
                time.sleep(1)
        except KeyboardInterrupt:
                GPIO.output(RelayPin, False)
                print("ancled program.")
                
        except:
                raise
        finally:       
                # flagWorking = False
                # destroy()
                # cv2.destroyAllWindows()
                GPIO.output(RelayPin, False)
                GPIO.cleanup() 