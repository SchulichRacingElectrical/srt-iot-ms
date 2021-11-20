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
    self.socket.connect((self.hw_address, 80))

  def transmit_message(self, message):
    # TODO
    # Do processing
    # throw exception for bad message format or other errors
    sent = self.socket.send(message)
    return sent != 0