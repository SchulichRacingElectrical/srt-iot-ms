# Copyright Schulich Racing FSAE
# Written By Abod Abbas, Justin Tijunelis

import os
import redis
import json

class RedisPublisher:
  def __init__(self, key, thing_id):
    self.api_key = key
    self.thing_id = thing_id
    self.redis_db = redis.Redis(
      host=os.getenv('REDIS_URL'), 
      port=os.getenv('REDIS_PORT'), 
      username=os.getenv('REDIS_USERNAME'), 
      password=os.getenv('REDIS_PASSWORD')
    )

  def publish_connection(self):
    if not (self.redis_db.execute_command('JSON.GET', f'THING_{self.thing_id}')): 
      self.redis_db.execute_command(
        'JSON.SET', 
        f'THING_{self.thing_id}', 
        '.', 
        json.dumps({
          "api_key": self.api_key, 
          "active": True
        })
      )
      self.redis_db.publish(
        f'THING_{self.thing_id}', 
        json.dumps({"active": True, "THING": self.thing_id})
      )
      # On subscriber, create data reading session

  def publish_disconnection(self):
    self.redis_db.execute_command(
      'JSON.SET', 
      f'THING_{self.thing_id}', 
      '.active', 
      f'false'
    )
    self.redis_db.publish(
      f'THING_{self.thing_id}', 
      json.dumps({
        "active": False, 
        "THING": self.thing_id
      })
    ) 
    # On subscriber, read all data, write to DB, delete redis

  async def publish_snapshots(self, snapshots):
    snapshots_string = ""
    for snapshot in snapshots:
      snapshots_string += '"' + json.dumps(snapshot).replace('"', '').replace(" ", "") + '" '
      print(json.loads(json.dumps(snapshot).replace('"', '').replace(" ", "")))
    self.redis_db.execute_command(f'RPUSH THING_{self.thing_id}_DATA {snapshots_string}')