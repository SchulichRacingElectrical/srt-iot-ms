# Copyright Schulich Racing, FSAE
# Written by Justin Tijunelis

import os
import socketio

class SessionEmitter:
  def __init__(self, thing_id):
    self.thing_id = thing_id
    self.sio = None
    self.room_created = False

  def start(self, key):
    if self.sio == None:
      try:
        self.sio = socketio.Client(reconnection=False)
        self.sio.connect(os.getenv('GATEWAY_ROUTE'), headers={"key": key})
        self.sio.emit('new room', {"thingId": self.thing_id, "secret": os.getenv('NEW_ROOM_SECRET')})

        @self.sio.on('room created')
        def on_room_created():
          self.room_created = True

        @self.sio.on('room creation error')
        def on_room_creation_error():
          self.stop()

        # TODO: Handle reconnection?
      except:
        self.stop()

  def emit_data(self, data):
    if self.sio != None and self.room_created:
      self.sio.emit('data', data)

  def stop(self):
    if self.sio != None:
      self.sio.disconnect()
      self.sio = None
      self.room_created = False