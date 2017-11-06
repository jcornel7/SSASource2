import json
import os
import random
from random import randint
import shutil

infobase = "/home/pi/device-info"

region = random.choice(['emea', 'amer', 'apac'])

files = os.listdir(os.path.join(infobase, region))
file_int = randint(1, len(files))
file_int = file_int-1

to_move = os.path.join(infobase, region, files[file_int])

print(to_move)

with open(to_move) as jfile:
    deviceinfo = json.load(jfile)



try:
    os.unlink('/tmp/deviceinfo.json')
except OSError:
    pass


shutil.move(to_move, "/tmp/deviceinfo.json")

print(deviceinfo['city'], deviceinfo['region'])
