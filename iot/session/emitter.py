# Copyright Schulich Racing, FSAE
# Written by Justin Tijunelis

import os
import socketio

class SessionEmitter:
  def __init__(self, thing_id, key):
    self.thing_id = thing_id
    self.api_key = key
    self.sio = None
    self.room_created = False

  def start(self):
    if self.sio == None:
      try:
        self.sio = socketio.Client()
        self.sio.connect(os.getenv('GATEWAY_ROUTE'), headers={apiKey: self.api_key})
        self.sio.emit('new room', self.thing_id)

        @self.sio.on('room created')
        def on_room_created():
          self.room_created = True

        @self.sio.on('room creation error')
        def on_room_creation_error():
          self.stop()
      except:
        self.sio = None
        print("Socket.io connection failed.")

  def emit_data(self, data):
    if self.sio != None and self.room_created:
      self.sio.emit('data', data)

  def stop(self):
    if self.sio != None:
      self.sio.disconnect()
      self.sio = None
      self.room_created = False