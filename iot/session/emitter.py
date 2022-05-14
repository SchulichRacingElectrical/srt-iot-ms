# Copyright Schulich Racing, FSAE
# Written by Justin Tijunelis

import os
import socketio

class SessionEmitter:
  def __init__(self, thing_id):
    self.thing_id = thing_id
    self.connected = False
    self.sio = None

  def start(self):
    if self.sio == None and not self.connected:
      try:
        self.sio = socketio.Client()
        self.sio.connect(os.getenv('GATEWAY_SOCKET_ROUTE'))

        @self.sio.event
        def connect():
          self.connected = True
          self.sio.emit('new room', self.thing_id)

        @self.sio.event
        def disconnect():
          self.connected = False
      except:
        print("Socket.io connection failed.")

  def emit_data(self, data):
    if self.connected:
      self.sio.emit('data', data)

  def stop(self):
    if self.connected:
      self.sio.emit('delete room', self.thing_id)
      self.sio.disconnect()