# Copyright Schulich Racing FSAE
# Written By Abod Abbas, Justin Tijunelis

import os
import redis
import json

class RedisPublisher:
  def __init__(self):
    self.redis_db = redis.Redis(
      host=os.getenv('REDIS_URL'), 
      port=os.getenv('REDIS_PORT'), 
      username=os.getenv('REDIS_USERNAME'), 
      password=os.getenv('REDIS_PASSWORD')
    )
    self.first_data = False

  def publish_message(self, message, api_key, thing_id, data):
    if message == "connection":
      # If existing, we must wait! Figure out what to do
      if not (self.redis_db.execute_command('JSON.GET', f'THING_{thing_id}')):
        self.redis_db.execute_command('JSON.SET', f'THING_{thing_id}', '.', json.dumps({"api_key": api_key, "active": True, "data": []}))
        self.redis_db.publish(f'THING_{thing_id}', json.dumps({"active": True, "THING": thing_id}))
        # TODO: Start batch insert session on subsriber. 
    elif message == "snapshot":
      self.redis_db.execute_command('JSON.ARRAPPEND', f'THING_{thing_id}', '.data', json.dumps(data))
      self.redis_db.publish(f'THING_{thing_id}', json.dumps(data))
      # TODO: Create batch insert on subscriber.
    elif message == "disconnection" or message == "error":
      self.redis_db.execute_command('JSON.SET', f'THING_{thing_id}', '.active', f'false')
      response = {"active": False, "THING": thing_id, "error": message == "error"}
      self.redis_db.publish(f'THING_{thing_id}', json.dumps(response))
      # TODO: Receive on subscriber end, enter all data, generate csv. 

# Singleton
publisher = RedisPublisher()