#!/usr/bin/env python

import time

from LIS3DH import LIS3DH
import RPi.GPIO as GPIO
import Adafruit_DHT

#  configure the library to use pin labels from the original SOC
GPIO.setmode(GPIO.BCM)

#  aka board pin #29, BCM pin #5
BUTTON_PIN = 5

#  Configure the pin to be an input pin, and if there is no signal make sure
#  it reads low by default by using internal pulldown
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

dht_sensor = Adafruit_DHT.DHT22
pin = 18

def main():
    sensor = LIS3DH()
    sensor.setRange(LIS3DH.RANGE_2G)
    while True:
        x = sensor.getX()
        y = sensor.getY()
        z = sensor.getZ()
        button_pressed = GPIO.input(BUTTON_PIN)== 1
        light_level = sensor.getADC(sensor.ADC_1)

        humidity, temperature = Adafruit_DHT.read_retry(dht_sensor, pin)
        if humidity is not None and temperature is not None:
                print('temp={0:0.1f}*C  humidity={1:0.1f}% '.format(temperature, humidity))

        print("light: %.6f\t  button: %s  orientation: X: %.6f\tY: %.6f\tZ: %.6f" %
                (light_level, button_pressed, x,y,z))

        time.sleep(.2)

if __name__ == "__main__":
    main()