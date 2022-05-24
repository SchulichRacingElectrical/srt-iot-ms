# Copyright Schulich Racing FSAE
# Written By Abod Abbas and Justin Tijunelis

import json
import os

import redis
from dotenv import load_dotenv

load_dotenv()

client = redis.Redis(
    host=os.environ["REDIS_URL"],
    port=os.environ["REDIS_PORT"],
    username=os.environ["REDIS_USERNAME"],
    password=os.environ["REDIS_PASSWORD"],
)

env = "SIN_1"

p = client.pubsub()
p.subscribe(env)

while True:
    message = p.get_message()
    if message and not message["data"] == 1:
        json_message = json.loads(message["data"].decode("utf-8"))
        if "active" in json_message:
            # Either connection or disconnection
            if json_message["active"]:
                print("We got a connection from a device with SIN: " + str(json_message["SIN"]))
            else:
                if json_message["error"]:
                    print(
                        "Device with SIN: "
                        + str(json_message["SIN"])
                        + " disconnected with an error."
                    )
                else:
                    print(
                        "Device with SIN: "
                        + str(json_message["SIN"])
                        + " disconnected with a timeout."
                    )

                    # Create an array of all the data
                    data = json.loads(
                        client.execute_command("JSON.GET", f'SIN_{json_message["SIN"]}')
                    )
                    data.pop("api_key")
                    data.pop("active")

                    # Flatten data
                    dataArray = []
                    for k, v in data.items():
                        updated = v
                        updated["timestamp"] = k
                        dataArray.append(updated)
                    dataArray.sort(key=lambda x: x["timestamp"])

                    # # Print it out
                    # print(dataArray)

                    # Delete all data from the database for this SIN
                    client.execute_command("JSON.DEL", f'SIN_{json_message["SIN"]}')

        else:
            # Data has arrived
            # Forward the data through socket.io
            # Don't worry about this for now.
            print(json_message)
