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
        self.redis_db.execute_command('JSON.SET', f'SIN_{serial_number}', '.', f'{{"api_key": {api_key}}}')
        self.redis_db.publish(f'SIN_{serial_number}', json.dumps({"active": True, "SIN": serial_number}))
    elif message == "snapshot":
      timestamp = data['timestamp']
      del data['timestamp']
      self.redis_db.execute_command('JSON.SET', f'SIN_{serial_number}', timestamp, json.dumps(data))
      self.redis_db.publish(f'SIN_{serial_number}', json.dumps(data))
    elif message == "disconnection" or message == "error":
      self.redis_db.execute_command('JSON.SET', f'SIN_{serial_number}', '.active', f'false')
      response = {"active": False, "SIN": serial_number, "error": message == "error"}
      self.redis_db.publish(f'SIN_{serial_number}', json.dumps(response))
