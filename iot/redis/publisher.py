# Copyright Schulich Racing FSAE
# Written By Abod Abbas, Justin Tijunelis

import os
import json
import redis

class RedisPublisher:
    def __init__(self, key, thing_id):
        self.api_key = key
        self.thing_id = thing_id
        self.redis_db = redis.Redis(
            host=os.getenv("REDIS_URL"),
            port=os.getenv("REDIS_PORT"),
            username=os.getenv("REDIS_USERNAME"),
            password=os.getenv("REDIS_PASSWORD"),
        )

    def publish_connection(self):
        self.redis_db.publish(
            "THING_CONNECTION", json.dumps({"active": True, "THING": self.thing_id})
        )
        self.redis_db.delete(f"THING_{self.thing_id}")

    def publish_disconnection(self):
        self.redis_db.publish(
            f"THING_{self.thing_id}", json.dumps({"active": False, "THING": self.thing_id})
        )

    async def push_snapshots(self, snapshots):
        snapshots_string = " ".join(
            [json.dumps(snapshot).replace(" ", "") for snapshot in snapshots]
        )
        self.redis_db.execute_command(f"RPUSH THING_{self.thing_id} {snapshots_string}")
