#!/usr/bin/env python

import RPi.GPIO as GPIO  # Import GPIO Module
from time import sleep  # Import sleep Module for timing

GPIO.setmode(GPIO.BCM)  # Configures pin numbering to Broadcom reference
GPIO.setwarnings(False)  # Disable Warnings
GPIO.setup(21, GPIO.OUT)  #Set our GPIO pin to output 
GPIO.output(21, False)  #Set output to off
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # Set GPIO to input with a  pull-down resistor
GPIO.add_event_detect(18, GPIO.RISING, bouncetime=200)  # Monitor GPIO pin for a rising edge and debounce for 200mS

while (True):
    if GPIO.event_detected(18):  # Check to see if button has been pushed
        activate = True
        while (activate is True):  # Execute this code until the button is pushed again
            GPIO.output(21, True)  # Turn LED on
            sleep(0.01)
            GPIO.output(21, False) # Turn LED off
            sleep(0.01)
            if GPIO.event_detected(18):  # Check for a 2nd button push
                activate = False
    else:
        GPIO.output(21, False)  # Turn LED off