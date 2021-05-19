import configparser
import time
import requests
import random
from string import ascii_letters

config = configparser.ConfigParser()
config.read('slave.config')

BASE_URL = config['MAIN']['MASTER_URL']
PING_DELAY = int(config['MAIN']['PING_FREQUENCY'])

node_name = ''.join(random.choices(ascii_letters, k=10))
COMPUTING = False
birth_time = time.time()

print(f'Node activated. Unique Node name: {node_name}')

while True:
    data = {'node_name': node_name,
            'is_computing': COMPUTING, 'alive_since': birth_time}
    resp = requests.post(BASE_URL+'/ping', data=data)
    print('RESPONSE:', resp.text)
    time.sleep(PING_DELAY)
