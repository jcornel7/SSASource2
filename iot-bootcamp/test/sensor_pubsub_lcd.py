from Adafruit_CharLCD import Adafruit_CharLCD

import json
import time
import socket
import os
import random
from random import randint
import shutil

from time import sleep, strftime
from datetime import datetime

from LIS3DH import LIS3DH
import RPi.GPIO as GPIO
import Adafruit_DHT

from google.cloud import pubsub

infobase = "/home/pi/device-info"

#LCD Init
lcd = Adafruit_CharLCD()
lcd.begin(16, 1)

#  configure the library to use pin labels from the original SOC
GPIO.setmode(GPIO.BCM)

#  aka board pin #29, BCM pin #5
BUTTON_PIN = 5

#  Configure the pin to be an input pin, and if there is no signal make sure
#  it reads low by default by using internal pulldown
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# set up the  dht22 sensor (temp,humidity)
dht_sensor = Adafruit_DHT.DHT22
pin = 18

def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]

def main():
    ip = get_ip_address()
    hostname = socket.gethostname()

    client = pubsub.Client(project="google.com:iot-bootcamp")
    topic = client.topic("bootcamp")

    sensor = LIS3DH()
    sensor.setRange(LIS3DH.RANGE_2G)
    data = {}

    while True:
	region = random.choice(['emea', 'amer', 'apac'])
	files = os.listdir(os.path.join(infobase, region))
        file_int = randint(1, len(files))
	file_int = file_int-1
	#print(file_int)
	
	to_move = os.path.join(infobase, region, files[file_int])

	with open(to_move) as jfile:
            device_config = json.load(jfile)

	d = datetime.utcnow()
        x = sensor.getX()
        y = sensor.getY()
        z = sensor.getZ()
        button_pressed = GPIO.input(BUTTON_PIN) == 1

        #  We "invert" the value by subtracting from 2700
        #  and convert to integer
        light_level = 2700 - int(sensor.getADC(sensor.ADC_1))

	# get data from the dht22 sensor
	humidity, temperature = Adafruit_DHT.read_retry(dht_sensor, pin)

        data['device_id'] = device_config['id']
	
	if ip is not None:
		data['ip'] = ip
        else:
		data['ip'] = "Unknown"

        data['city'] = device_config['city']
        data['country'] = device_config['country']
        data['region'] = device_config['region']
        data['lat'] = device_config['lat']
        data['long'] = device_config['lng']
        data["timestamp"] = d.isoformat("T") + "Z"
        data['light_level'] = light_level
        data['button_pressed'] = button_pressed
        data['orientation'] = {'x': x, 'y': y, 'z': z}

	if humidity is not None and temperature is not None:
                data['temperature'] = str(round(temperature, 2))
                data['humidity'] = str(round(humidity, 2))
        else:
                data['temperature'] = 0
                data['humidity'] = 0
	
	if data['lat'] < 10:
		data['temperature'] = float(data['temperature']) + round(random.uniform(10,40), 1)
		data['humidity'] = float(data['humidity']) + round(random.uniform(10, 38), 1)
	else:
		data['temperature'] = float(data['temperature']) - round(random.uniform(5, 20), 1)
		data['humidity'] = float(data['humidity']) - round(random.uniform(10, 25), 1)

        data['ip_address'] = ip
        data['hostname'] = hostname	
	
	lcd.clear()
        lcd.message('IP%s\n' % (data['ip']))
        lcd.message('H:%s' % (data['hostname']))
	time.sleep(4)

        lcd.clear()
        lcd.message('%s %s\n' % (data['city'],data['region']))
        lcd.message('%s\n' % (data['country']))
        time.sleep(4)

	lcd.clear()
    	lcd.message(datetime.now().strftime('%b %d  %H:%M:%S\n'))
    	lcd.message('T %s H %s' % (data['temperature'],data['humidity']))
	time.sleep(4)

	lcd.clear()
        lcd.message('Light %s\n' % (str(round(light_level, 0))))
        lcd.message('%s %s %s' % (str(round(x, 2)),str(round(y, 2)),str(round(z, 2))))
	time.sleep(4)

	lcd.clear()
        lcd.message('Button %s\n' % (data['button_pressed']))
        lcd.message('LT:%s LG:%s' % (str(round(data['lat'], 1)),str(round(data['long'], 1))))

	print(data)

	try:
                topic.publish(json.dumps(data).encode('utf-8'), timestamp=data["timestamp"])
        except:
                print("Failed to submit to PubSub. Trying again...")
                pass

        time.sleep(1)

if __name__ == "__main__":
    main()
