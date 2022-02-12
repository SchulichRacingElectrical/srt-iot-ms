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

    # dct = {'name':"ABC", 'Age': 25, "profession":"soft dev"}
    # print(self.redis_db.execute_command('JSON.SET', 'abc', '.', json.dumps(dct)))

  def publish_message(self, message, api_key, serial_number, data):
    # TODO data['ts']
    if message == "connection":
      if not (self.redis_db.execute_command('JSON.GET', f'SIN_{serial_number}')):
        self.redis_db.execute_command('JSON.SET', f'SIN_{serial_number}', '.', '{"counter": 1}')
        self.redis_db.execute_command('JSON.SET', f'SIN_{serial_number}', '.Data_1', json.dumps(data))
        # self.redis_db.execute_command('JSON.SET', f'SIN_{serial_number}', '.counter', 1)
        
        self.redis_db.publish(f'SIN_{serial_number}', json.dumps(data))
        print(self.redis_db.execute_command('JSON.GET', f'SIN_{serial_number}', '.Data_1'))

    elif message == "snapshot":
      counter  = int(self.redis_db.execute_command('JSON.GET', f'SIN_{serial_number}', '.counter'))
      
      if counter:
        counter = counter +1

        self.redis_db.execute_command('JSON.SET', f'SIN_{serial_number}', f'.DATA_{counter}', json.dumps(data))
        self.redis_db.execute_command('JSON.SET', f'SIN_{serial_number}', '.counter', counter)
        self.redis_db.publish(f'SIN_{serial_number}', json.dumps(data))

    elif message == "disconnection":
      self.redis_db.execute_command('JSON.DEL', f'SIN_{serial_number}')

    elif message == "error":
      pass

  # def subscribe_message():
  #   # This is executed when a new set of data is put into the db
  #   pass


dict = {'name': 'ABC', 'Age': 25, 'profession': 'soft dev'}
publisher = Publisher()
publisher.publish_message("connection", 2, 1, dict)
publisher.publish_message("snapshot", 2, 1, dict)
publisher.publish_message("disconnection", 2, 1, dict)


# SIN_1
#   Data 1
#   Data 2
# SIN_2
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

# Requirements:
# 1) Have a data store for each serial number, when the message is equal to "connection"
# 2) When there is a disconnection everything for that serial number is cleared off redis
# 3) On error just ignore for now
# 4) when a new data snapshot comes in that should be pushed corresponding serial number data set
# 5) when that new published snapshot is pushed the subscribers should only recieve the new snapshot only
# 6) bonus: be able to sort the snapshot for each serial number by snapshot, python library
