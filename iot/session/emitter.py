# Copyright Schulich Racing, FSAE
# Written by Justin Tijunelis

import os
import time
import socketio
import threading

class SessionEmitter:
    def __init__(self, key, thing_id, sensor_list):
        self.api_key = key
        self.thing_id = thing_id
        self.sensor_frequency_map = {}
        self.transmission_frequency = 0
        for sensor in sensor_list:
            self.sensor_frequency_map[str(sensor["smallId"])] = sensor["frequency"]
            if sensor["frequency"] > self.transmission_frequency:
                self.transmission_frequency = sensor["frequency"]
        self.sio = None
        self.room_active = False
        self.current_datum = {}

    def start(self):
        if self.sio != None: return
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
                self.room_active = True
                self.emit_thread = None

            @self.sio.on("room creation error")
            def on_room_creation_error():
                self.stop()

            @self.sio.on("disconnect")
            def disconnect():
                self.sio = None
                self.room_active = False
                if self.emit_thread != None:
                    self.emit_thread.join()

            # TODO: Handle reconnection - Recreate the new room
        except:
            self.stop()

    def push_data(self, data):
        if self.sio == None or not self.room_active: return
        if self.transmission_frequency <= int(os.getenv("MAX_STREAMING_FREQUENCY")):
            self.sio.emit("data", data)
        else:
            for key in data: self.current_datum[key] = data[key]
            if self.emit_thread == None:
                self.sio.emit("data", data)
                self.emit_thread = threading.Thread(target=self.__emit_data)
                self.emit_thread.start()
                
    def stop(self):
        if self.sio == None: return
        self.sio.disconnect()
        self.room_active = False
        if self.emit_thread != None:
            self.emit_thread.join()

    def __emit_data(self):
        current_time = 0
        queued_datum = {}
        last_timestamp = -1
        while self.room_active:
            # Populate the queued data
            if "ts" in self.current_datum:
                queued_datum["ts"] = self.current_datum["ts"]
            for key in self.sensor_frequency_map:
                if current_time % round(1000 / self.sensor_frequency_map[key]) == 0:
                    if key in self.current_datum:
                        queued_datum[key] = self.current_datum[key]

            # Send data on MAX_STREAMING_FREQUENCY syncronization
            if current_time % round(1000 / int(os.getenv("MAX_STREAMING_FREQUENCY"))) == 0:
                if len(queued_datum) > 1 and queued_datum["ts"] != last_timestamp:
                    self.sio.emit("data", queued_datum)
                    last_timestamp = queued_datum["ts"]
                    queued_datum = {}

            # Sleep at same frequency as hardware in loop thread
            time.sleep(1 / 1000)
            current_time += 1
