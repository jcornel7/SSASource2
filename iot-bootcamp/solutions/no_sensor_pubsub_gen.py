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

from google.cloud import pubsub

infobase = "/home/pi/device-info"

def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]

def main():
    ip = get_ip_address()
    hostname = socket.gethostname()

    client = pubsub.Client(project="google.com:iot-bootcamp")
    topic = client.topic("bootcamp")

    data = {}

    while True:
	region = random.choice(['emea', 'amer', 'apac'])
	files = os.listdir(os.path.join(infobase, region))
        file_int = randint(1, len(files))
	file_int = file_int-1
	
	to_move = os.path.join(infobase, region, files[file_int])

	with open(to_move) as jfile:
            device_config = json.load(jfile)

	d = datetime.utcnow()
        x = round(random.uniform(-4,4), 5)
        y = round(random.uniform(-4,4), 5)
        z = round(random.uniform(-4,4), 5)
        button_pressed = random.choice(['true', 'false'])
        light_level = int(random.uniform(800,1200))
	humidity = round(random.uniform(10,70), 2)
	temperature = round(random.uniform(10,70), 2)

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
	
	print(data)

	try:
		topic.publish(json.dumps(data).encode('utf-8'), timestamp=data["timestamp"])
	except:
		print("Failed to submit to PubSub. Trying again...")
		pass

        time.sleep(1)

if __name__ == "__main__":
    main()
