# Copyright Schulich Racing FSAE
# Written By Justin Tijunelis

import os
import redis

class Publisher:
  def __init__(self):
    url = os.getenv('REDIS_URL')
    port = os.getenv('REDIS_PORT')
    self.redis_db = redis.Redis(host=url, port=port, db=0)

  def publish_message(self, message, api_key, serial_number, data):
    if message == "connection":
      pass
    elif message == "snapshot":
      pass
    elif message == "disconnection":
      pass
    elif message == "error":
      pass

publisher = Publisher()