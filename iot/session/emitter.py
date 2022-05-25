# Copyright Schulich Racing, FSAE
# Written by Justin Tijunelis

import os
import time
import socketio

class SessionEmitter:
    def __init__(self, key, thing_id, frequency):
        self.api_key = key
        self.thing_id = thing_id
        self.sio = None
        self.room_created = False
        self.frequency = frequency
        self.last_send_time = round(time.time() * 1000) 
        self.queued_data = {}

    def start(self):
        if self.sio == None:
            try:
                self.sio = socketio.Client(reconnection=False)
                self.sio.connect(os.getenv("GATEWAY_ROUTE"), headers={"key": self.api_key})
                self.sio.emit(
                    "new room", 
                    {
                        "thingId": self.thing_id, 
                        "secret": os.getenv("NEW_ROOM_SECRET")
                    }
                )

                @self.sio.on("room created")
                def on_room_created():
                    self.room_created = True
                    # Create new thread

                @self.sio.on("room creation error")
                def on_room_creation_error():
                    self.stop()

                @self.sio.on("disconnect")
                def disconnect():
                    self.sio = None
                    self.room_created = False

                # TODO: Handle reconnection - Recreate the new room
            except:
                self.stop()

    def emit_data(self, data): # We send data at a max of MAX_STREAMING_FREQUENCY
        if self.sio != None and self.room_created:
            if self.frequency <= int(os.getenv("MAX_STREAMING_FREQUENCY")):
                self.sio.emit("data", data)
            else:
                current_time = round(time.time() * 1000)
                time_diff = current_time - self.last_send_time
                if time_diff > (1000 / int(os.getenv("MAX_STREAMING_FREQUENCY"))):
                    for key in self.queued_data:
                        if key not in data:
                            data[key] = self.queued_data[key]
                    self.sio.emit("data", data)
                    self.last_send_time = current_time
                    self.queued_data = {}
                else:
                    for key in data:
                        if key == "ts": continue
                        self.queued_data[key] = data[key]

    def stop(self):
        if self.sio != None:
            self.sio.disconnect()
