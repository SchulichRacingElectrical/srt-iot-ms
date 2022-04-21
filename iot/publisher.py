# Copyright Schulich Racing FSAE
# Written By Abod Abbas, Justin Tijunelis

import os
import redis
import json

class Publisher:
  def __init__(self):
    self.redis_db = redis.Redis(
      host=os.getenv('REDIS_URL'), 
      port=os.getenv('REDIS_PORT'), 
      username=os.getenv('REDIS_USERNAME'), 
      password=os.getenv('REDIS_PASSWORD')
    )

  def publish_message(self, message, api_key, thing_id, data):
    if message == "connection":
      if not (self.redis_db.execute_command('JSON.GET', f'THING_{thing_id}')):
        self.redis_db.execute_command('JSON.SET', f'THING_{thing_id}', '.', f'{{"api_key": {api_key}}}')
        self.redis_db.publish(f'THING_{thing_id}', json.dumps({"active": True, "THING": thing_id}))
    elif message == "snapshot":
      timestamp = data['timestamp']
      del data['timestamp']
      self.redis_db.execute_command('JSON.SET', f'THING_{thing_id}', timestamp, json.dumps(data))
      self.redis_db.publish(f'THING_{thing_id}', json.dumps(data))
    elif message == "disconnection" or message == "error":
      self.redis_db.execute_command('JSON.SET', f'THING_{thing_id}', '.active', f'false')
      response = {"active": False, "THING": thing_id, "error": message == "error"}
      self.redis_db.publish(f'THING_{thing_id}', json.dumps(response))

# Singleton
publisher = Publisher()