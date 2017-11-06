#!/usr/bin/env python

import time

import RPi.GPIO as GPIO


#  configure the library to use pin labels from the original SOC
GPIO.setmode(GPIO.BCM)

#  aka board pin #29, BCM pin #5
BUTTON_PIN = 5

#  Configure the pin to be an input pin, and if there is no signal make sure
#  it reads low by default by using internal pulldown
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def main():
    while True:
        print(GPIO.input(BUTTON_PIN))
        time.sleep(.5)

if __name__ == "__main__":
    main()