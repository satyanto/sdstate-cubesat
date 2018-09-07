import RPi.GPIO as GPIO
import time
GPIO.setmomde(GPIO.BOARD)
GPIO.setup(21, GPIO.OUT)

while true:
    GPIO.output(21,True)
    time.sleep(1.5)
    GPIO.output(21,False)
    time.sleep(1.5)

GPIO.cleanup()
