# Copyright Schulich Racing FSAE
# Written By Justin Tijunelis

import os
import redis
import json
import math
import hjson

QUEUE_TIME_TO_STORE = 5

class RedisReader:
  def __init__(self):
    self.redis_db = redis.Redis(
      host=os.getenv('REDIS_URL'), 
      port=os.getenv('REDIS_PORT'), 
      username=os.getenv('REDIS_USERNAME'), 
      password=os.getenv('REDIS_PASSWORD')
    )
    self.queued_snapshots = {}

  # TODO: Test this
  def fetch_thing_data(self, thing_id):
    if thing_id in self.queued_snapshots:
      # Read data from redis
      stored_data_list = hjson.loads(self.redis_db.get(thing_id)) # TODO: Don't think this actually works
      if len(stored_data_list) == 0:
        return None

      # Append the queued data if needed
      current_data = stored_data_list
      last_redis_timestamp = stored_data_list[:-1]["ts"]
      if len(self.queued_snapshots) > 0:
        queue_start_timestamp = self.queued_snapshots[thing_id]["snapshots"][0]["ts"]
        queue_end_timestamp = self.queued_snapshots[thing_id]["snapshots"][-1]["ts"]
        if last_redis_timestamp >= queue_end_timestamp:
          pass
        elif last_redis_timestamp <= queue_start_timestamp:
          # We have a gap in the data
          current_data += self.queued_snapshots[thing_id]["snapshots"]
        else:
          frequency = self.queued_snapshots[thing_id]["max_queue_size"] / QUEUE_TIME_TO_STORE
          cut_index = (last_redis_timestamp - queue_start_timestamp) / math.ceil(1000 / frequency)
          current_data += self.queued_snapshots[thing_id]["snapshots"][cut_index:]

      print(current_data) # FOR TESTING
      return current_data
    else:
      return None

  def init_thing_queue(self, thing):
    if thing.thing_id not in self.queued_snapshots:
      self.queued_snapshots[thing.thing_id] = {
        "snapshots": [],
        # Store past seconds to merge with db data if it has not been written yet
        "max_queue_size": thing.get_transmission_frequency() * QUEUE_TIME_TO_STORE,
      }

  def push_queue_snapshot(self, thing_id, snapshot):
    if thing_id in self.queued_snapshots:
      self.queued_snapshots[thing_id]["snapshots"].append(snapshot)
      size = len(self.queued_snapshots[thing_id]["snapshots"])
      if size == self.queued_snapshots[thing_id]["max_queue_size"]:
        self.queued_snapshots[thing_id].pop(0)

  def destory_thing_queue(self, thing_id):
    if thing_id in self.queued_snapshots:
      del self.queued_snapshots[thing_id]

reader = RedisReader()