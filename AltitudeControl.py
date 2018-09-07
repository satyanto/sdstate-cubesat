#!/usr/bin/python
"""
controlAltitude.py

Written by Calvin Kielas-Jensen
calvin.kielasjensen@jacks.sdstate.edu

Controls the altitude of the CubeSat high altitude balloon by opening a
solenoid valve depending on the altitude the balloon is at. It uses a PD
controller to achieve this. If the maximum time has been reached, the solenoid
valve will remain open as to let all of the helium out of the balloon.

NOTE: This uses system time, not an external RTC. This means that if the pi 
loses power, the time may behave unexpectedely.
"""
import pid
import RPi.GPIO as GPIO
import time

import mpl3115a2

DEBUG = True

# IMPORTANT CONSTANTS FOR CUBESAT TEAM TO MODIFY
KP = 1*10^-8                 # Proportional gain
KI = 0                  # Integral gain
KD = 3*10^-4                # Derivative gain
MIN_ALT = 300        # Minimum altitude to start the controller (m)
MAX_ALT = 400.2        # Set point for the altitude (m)
KILL_TIME = 1     #Time at which to hold the valve open (hr)
VALVE_PIN = 7           # Which GPIO board pin to use to control the solenoid
                        # DO NOT CHANGE VALVE_PIN TO 3 or 5. IF YOU DO, IT
                        # WILL BREAK THE I2C BUS AND YOU'LL HAVE TO RESTART
                        # THE PI.
CTRL_PER = 1    # Period at which the controller runs (sec)
CTRL_THRESH = 0.000167       # Control value threshold to open the solenoid

def main():
    # Need to do this try and finally so that we guarantee we release control
    # of the GPIO pins (the RPi.GPIO library is pretty awful at protecting
    # hardware)
    try:
        # Sensor
        mpl = mpl3115a2.MPL3115A2()
        # Controller
        controller = pid.PID(KP, KI, KD)
        controller.setSampleTime(CTRL_PER)
        controller.SetPoint=MAX_ALT
        # GPIO stuff
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(VALVE_PIN, GPIO.OUT, initial=GPIO.LOW)
        
        startTime = time.time()
        
        # Wait for altitude to start the controller and do nothing while waiting
        while True:
            while not mpl.ready():
                pass
            alt, cTemp, fTemp = mpl.getTempAlt()
            if alt >= MIN_ALT:
                break
            if DEBUG:
                print(
                """
Altitude: {}
Temp (C): {}
Temp (F): {}
                """.format(alt, cTemp, fTemp))
                
        # Run the controller and wait for KILL_TIME to open the valve
        while True:
            alt, cTemp, fTemp = mpl.getTempAlt()
            timer = (time.time() - startTime) / (60*60)
            if timer >= KILL_TIME:
                break
            
            controller.update(alt)
            
            if -controller.output >= 0.5*CTRL_THRESH:
                GPIO.output(VALVE_PIN, GPIO.HIGH)
            else:
                GPIO.output(VALVE_PIN, GPIO.LOW)
                
            if DEBUG:
                print(
                """
Altitude: {}
Temp (C): {}
Temp (F): {}
Control Value: {}
Time:{}
                """.format(alt, cTemp, fTemp, controller.output,timer))

        # Open the valve forever
        while True:
            GPIO.output(VALVE_PIN, GPIO.HIGH)
    finally:
        GPIO.cleanup()

if __name__ == '__main__':
    main()
\
