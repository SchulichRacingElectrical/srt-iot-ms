# Copyright Schulich Racing FSAE
# Written By Justin Tijunelis

import os
import math
import json
import redis

DOWNLOAD_RATE = 12.5 # MBps

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
        if thing_id not in self.queued_snapshots: return None

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
        if len(stored_data_list) == 0: return None

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
                cut_index = math.ceil((last_redis_timestamp - queue_start_timestamp) / math.ceil(
                    1000 / self.queued_snapshots[thing_id]["frequency"]
                ))
                current_data += self.queued_snapshots[thing_id]["snapshots"][cut_index:]

        # Decimate the data to a max of MAX_STREAMING_FREQUENCY Hz
        if self.queued_snapshots[thing_id]["frequency"] > int(os.getenv("MAX_STREAMING_FREQUENCY")):
            # Create maps to improve efficiency
            current_data_map = {}
            for datum in current_data: current_data_map[datum["ts"]] = datum
            sensor_frequency_map = self.queued_snapshots[thing_id]["sensor_frequency_map"]

            # Populate the decimated data
            decimated_data = []
            last_timestamp = -1
            queued_datum = {}
            current_datum = current_data[0]
            for current_time in range(0, current_data[-1]["ts"] + 1):
                # Set the next piece of data if the frequency aligned
                if current_time in current_data_map:
                    current_datum = current_data_map[current_time]

                # Populate the queued data
                queued_datum["ts"] = current_datum["ts"]
                for key in sensor_frequency_map:
                    if current_time % round(1000 / sensor_frequency_map[key]) == 0:
                        if key in current_datum:
                            queued_datum[key] = current_datum[key]
                
                # Insert the data on frequency alignment
                if current_time % round(1000 / int(os.getenv("MAX_STREAMING_FREQUENCY"))) == 0:
                    if len(queued_datum) > 1 and queued_datum["ts"] != last_timestamp:
                        decimated_data.append(queued_datum)
                        last_timestamp = queued_datum["ts"]
                        queued_datum = {}

            current_data = decimated_data

        return current_data

    def init_thing_queue(self, thing):
        if thing.thing_id not in self.queued_snapshots:
            sensor_frequency_map = {}
            for sensor in thing.sensor_list:
                sensor_frequency_map[str(sensor["smallId"])] = sensor["frequency"]
            self.queued_snapshots[thing.thing_id] = {
                "snapshots": [],
                "max_queue_size": round(thing.get_transmission_frequency()),
                "frequency": thing.get_transmission_frequency(),
                "sensor_frequency_map": sensor_frequency_map,
                "db_size": 0
            }

    def push_queue_snapshot(self, thing_id, snapshot):
        if thing_id in self.queued_snapshots:
            # Append the data and update the db size
            self.queued_snapshots[thing_id]["snapshots"].append(snapshot)
            self.queued_snapshots[thing_id]["db_size"] += len(json.dumps(snapshot)) * pow(10, -6)\
            
            # Update the max queue size based on how long it will take to download the data
            download_time = self.queued_snapshots[thing_id]["db_size"] / DOWNLOAD_RATE
            self.queued_snapshots[thing_id]["max_queue_size"] = min(
                round(self.queued_snapshots[thing_id]["frequency"]), 
                round(self.queued_snapshots[thing_id]["frequency"] * download_time)
            )

            # Update the snapshot queue size if needed
            size = len(self.queued_snapshots[thing_id]["snapshots"])
            if size == self.queued_snapshots[thing_id]["max_queue_size"]:
                self.queued_snapshots[thing_id]["snapshots"].pop(0)

    def destory_thing_queue(self, thing_id):
        if thing_id in self.queued_snapshots:
            del self.queued_snapshots[thing_id]

reader = RedisReader()
