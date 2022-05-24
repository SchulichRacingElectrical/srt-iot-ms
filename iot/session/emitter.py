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

    def start(self):
        if self.sio == None:
            try:
                self.sio = socketio.Client(reconnection=False)
                self.sio.connect(os.getenv("GATEWAY_ROUTE"), headers={"key": self.api_key})
                self.sio.emit(
                    "new room", {"thingId": self.thing_id, "secret": os.getenv("NEW_ROOM_SECRET")}
                )

                @self.sio.on("room created")
                def on_room_created():
                    self.room_created = True

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

    def emit_data(self, data): # We send data at a max of 20 Hz
        if self.sio != None and self.room_created:
            if self.frequency <= 20:
                self.sio.emit("data", data)
            else:
                current_time = round(time.time() * 1000)
                time_diff = current_time - self.last_send_time
                if time_diff > 50:
                    self.sio.emit("data", data)
                    self.last_send_time = current_time

    def stop(self):
        if self.sio != None:
            self.sio.disconnect()
