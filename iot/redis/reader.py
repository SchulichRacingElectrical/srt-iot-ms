# Copyright Schulich Racing FSAE
# Written By Justin Tijunelis

import math
import os
import json
import redis

QUEUE_TIME_TO_STORE = 5

class RedisReader:
    def __init__(self):
        self.redis_db = redis.Redis(
            host=os.getenv("REDIS_URL"),
            port=os.getenv("REDIS_PORT"),
            username=os.getenv("REDIS_USERNAME"),
            password=os.getenv("REDIS_PASSWORD"),
        )
        self.queued_snapshots = {}

    def fetch_thing_data(self, thing_id):
        if thing_id in self.queued_snapshots:
            # Read data from redis
            stored_data_list = json.loads(
                "[" + 
                ",".join(
                    map(
                        lambda x: x.decode('utf-8'), 
                        self.redis_db.lrange("THING_" + thing_id, 0, -1)
                    )
                ) + 
                "]"
            )
            if len(stored_data_list) == 0:
                return None

            # Append the queued data if needed
            current_data = stored_data_list
            last_redis_timestamp = int(stored_data_list[-1]["ts"])
            if len(self.queued_snapshots[thing_id]["snapshots"]) > 0:
                queue_start_timestamp = int(self.queued_snapshots[thing_id]["snapshots"][0]["ts"])
                queue_end_timestamp = int(self.queued_snapshots[thing_id]["snapshots"][-1]["ts"])
                if last_redis_timestamp >= queue_end_timestamp:
                    pass
                elif last_redis_timestamp <= queue_start_timestamp:
                    # We have a gap in the data
                    current_data += self.queued_snapshots[thing_id]["snapshots"]
                else:
                    frequency = self.queued_snapshots[thing_id]["max_queue_size"] / QUEUE_TIME_TO_STORE
                    cut_index = math.ceil((last_redis_timestamp - queue_start_timestamp) / math.ceil(
                        1000 / frequency
                    ))
                    current_data += self.queued_snapshots[thing_id]["snapshots"][cut_index:]

            # Decimate the data to a max of MAX_STREAMING_FREQUENCY Hz
            if self.queued_snapshots[thing_id]["frequency"] > int(os.getenv("MAX_STREAMING_FREQUENCY")):
                decimated_data = [current_data[0]]
                last_pushed_timestamp = decimated_data[0]["ts"]
                for datum in current_data:
                    current_timestamp = datum["ts"]
                    time_diff = current_timestamp - last_pushed_timestamp
                    if time_diff >= (1000 / int(os.getenv("MAX_STREAMING_FREQUENCY"))):
                        decimated_data.append(datum)
                        last_pushed_timestamp = current_timestamp
                current_data = decimated_data

            return current_data
        else:
            return None

    def init_thing_queue(self, thing):
        if thing.thing_id not in self.queued_snapshots:
            self.queued_snapshots[thing.thing_id] = {
                "snapshots": [],
                # Store past seconds to merge with db data if it has not been written yet
                # TODO: Should be a function of the size of the database as well
                "max_queue_size": thing.get_transmission_frequency() * QUEUE_TIME_TO_STORE,
                "frequency": thing.get_transmission_frequency(),
                "db_size": 0
            }

    def push_queue_snapshot(self, thing_id, snapshot):
        if thing_id in self.queued_snapshots:
            self.queued_snapshots[thing_id]["snapshots"].append(snapshot)
            self.queued_snapshots[thing_id]["db_size"] += len(json.dumps(snapshot))
            # TODO: Based on download speed, resolve how big the queue should be
            size = len(self.queued_snapshots[thing_id]["snapshots"])
            if size == self.queued_snapshots[thing_id]["max_queue_size"]:
                self.queued_snapshots[thing_id]["snapshots"].pop(0)

    def destory_thing_queue(self, thing_id):
        if thing_id in self.queued_snapshots:
            del self.queued_snapshots[thing_id]


reader = RedisReader()
