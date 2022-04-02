# Copyright Schulich Racing FSAE
# Written By Justin Tijunelis

import socket

"""
TCP communication with telemetry hardware. 
"""
class Transmitter:
  def __init__(self, hw_address):
    self.hw_address = hw_address
    self.__connect()

  def __connect(self):
    self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.socket.connect((self.hw_address, 4000))

  def transmit_message(self, message):
    split = message.split(',')
    if len(split[0]) == 0 and split[0].isdigit() and len(split) == 2:
      sent = self.socket.send(message)
      return sent != 0
    else:
      return False