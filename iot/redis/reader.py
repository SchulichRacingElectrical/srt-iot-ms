# Copyright Schulich Racing FSAE
# Written By Justin Tijunelis

import os
import redis

class RedisReader:
  def __init__(self):
    self.redis_db = redis.Redis(
      host=os.getenv('REDIS_URL'), 
      port=os.getenv('REDIS_PORT'), 
      username=os.getenv('REDIS_USERNAME'), 
      password=os.getenv('REDIS_PASSWORD')
    )

  def fetch_thing_data(self, thing_id):
    # TODO: Read from the redis database, parse data to only include that which is relevant
    # Return list of objects (should we format?)
    pass

  def fetch_thing_sensor_data(self, thing_id, sensor_ids):
    pass

  def fetch_sensor_data(self, thing_id, sensor_id):
    # TODO
    pass

reader = RedisReader()