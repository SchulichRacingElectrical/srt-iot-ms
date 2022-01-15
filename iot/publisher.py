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
    # TODO
    if message == "connection":
      pass
    elif message == "snapshot":
      pass
    elif message == "disconnection":
      pass
    elif message == "error":
      pass

# SIN 1
#   Data 1
#   Data 2
# SIN 2
#   Data 1
#   Data 2

# You will receive data in a snapshot message
# {"timestamp": 100, "0": 1.05, ""....}
# Put this data into redis
# Keep it in a format that 0-1000

# active sessions record
# Post serial numbers inside the active records on connection
# Remove the serial number on a disconnection
# Error -> Remove from the active records
# Have error messages record

publisher = Publisher()