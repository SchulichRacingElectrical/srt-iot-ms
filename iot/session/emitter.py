# Copyright Schulich Racing, FSAE
# Written by Justin Tijunelis

import os
import socketio

class SessionEmitter:
  def __init__(self, thing_id):
    self.thing_id = thing_id
    self.sio = None

  def start(self):
    if self.sio == None:
      try:
        self.sio = socketio.Client()
        self.sio.connect(os.getenv('GATEWAY_ROUTE'))
        # TODO: Wait for connection
        self.sio.emit('new room', self.thing_id)
      except:
        self.sio = None
        print("Socket.io connection failed.")

  def emit_data(self, data):
    if self.sio != None:
      self.sio.emit('data', data)

  def stop(self):
    if self.sio != None:
      self.sio.disconnect()
      self.sio = None