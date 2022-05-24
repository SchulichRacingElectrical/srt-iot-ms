# Copyright Schulich Racing FSAE
# Written By Justin Tijunelis

import json

import redis

env = "SIN_1"

url = "redis-16146.c239.us-east-1-2.ec2.cloud.redislabs.com"
port = 16146
client = redis.Redis(host=url, port=port, username="abod", password="Rahman252?")

p = client.pubsub()
p.subscribe(env)

while True:
    message = p.get_message()

    if message and not message["data"] == 1:
        message = json.loads(message["data"])
        print(f"Received command: {message}")
