# Copyright Schulich Racing FSAE
# Written By Justin Tijunelis

import os
import redis
import json

class Publisher:
  def __init__(self):
    # url = os.getenv('REDIS_URL')
    # port = os.getenv('REDIS_PORT')
    url = "redis-16146.c239.us-east-1-2.ec2.cloud.redislabs.com"
    port = 16146
    self.redis_db = redis.Redis(host=url, port=port, username="abod", password="Rahman252?")

  def publish_message(self, message, api_key, serial_number, data):
    if message == "connection":
      if not (self.redis_db.execute_command('JSON.GET', f'SIN_{serial_number}')):
        self.redis_db.execute_command('JSON.SET', f'SIN_{serial_number}', '.', f'{{"api_key": {api_key}, "active": true}}')
        self.redis_db.publish(f'SIN_{serial_number}', json.dumps(data))
    elif message == "snapshot":
        timestamp = data['timestamp']
        del data['timestamp']
        self.redis_db.execute_command('JSON.SET', f'SIN_{serial_number}', timestamp, json.dumps(data))
        self.redis_db.publish(f'SIN_{serial_number}', json.dumps(data))
    elif message == "disconnection":
      self.redis_db.execute_command('JSON.DEL', f'SIN_{serial_number}')
    elif message == "error":
      pass

publisher = Publisher()
publisher.publish_message("connection", 2, 1, {})
data = {'timestamp': 0, 0: 1, 1: 2, 2: 3, 3: 4, 4: 5}
publisher.publish_message("snapshot", 2, 1, data)
data = {'timestamp': 1, 0: 3, 1: 4, 2: 5, 3: 1000, 4: 500}
publisher.publish_message("snapshot", 2, 1, data)
# publisher.publish_message("disconnection", 2, 1, {})