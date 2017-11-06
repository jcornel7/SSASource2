#!/usr/bin/env python

import time
import socket

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
dht_pin = 18

def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]

def main():

    ip = get_ip_address()
    hostname = socket.gethostname()

    sensor = LIS3DH()
    sensor.setRange(LIS3DH.RANGE_2G)
    data = {}

    while True:
        x = sensor.getX()
        y = sensor.getY()
        z = sensor.getZ()
        button_pressed = GPIO.input(BUTTON_PIN)== 1
        light_level = sensor.getADC(sensor.ADC_1)

        humidity, temperature = Adafruit_DHT.read_retry(dht_sensor, dht_pin)
        if humidity is not None and temperature is not None:
                data['temperature'] = str(round(temperature, 2))
                data['humidity'] = str(round(humidity, 2))
        else:
                data['temperature'] = 0
                data['humidity'] = 0


        data['button_pressed'] = button_pressed
        data['orientation'] = {'x': x, 'y': y, 'z': z}

        data['ip_address'] = ip
        data['hostname'] = hostname

        print(data)

        time.sleep(.2)

if __name__ == "__main__":
    main()