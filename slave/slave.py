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
birth_time = time.time()

print(f'Node activated. Unique Node name: {node_name}')

while True:
    COMPUTING = bool(int(config['MAIN']['COMPUTING']))
    data = {'node_name': node_name,
            'is_computing': COMPUTING, 'alive_since': birth_time}
    resp = requests.post(BASE_URL+'/ping', data=data)
    if resp.status == 200:
        print('RESPONSE:', resp.text)
    elif resp.status_code == 202:
        print('Work Assigned')
        with open('./settings.json', 'w') as json_f:
            json_f.write(resp.text)
    time.sleep(PING_DELAY)
