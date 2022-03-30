# Copyright Schulich Racing FSAE
# Written By Justin Tijunelis, Camilla Abdrazakov, Jonathan Mulyk

import sys
import socket
import threading
import time
from iot.parser import Parser

CONNECTION_TIMEOUT = 10.0
MESSAGE_TIMEOUT = 3.0

"""
UDP variable frequency data receiver from telemetry hardware. 
"""
class Receiver:
  def __init__(self, sensors, coordinator):
    self.coordinator = coordinator
    self.connected = False
    self.parser = Parser(sensors)

  def start(self):
    self.soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
      self.soc.bind(('', 0))
      self.soc.settimeout(CONNECTION_TIMEOUT)
    except socket.error as msg:
      self.coordinator.notify("error")
      return -1
    self.udp_listener = threading.Thread(target=self.__read_data)
    self.udp_listener.start()
    _, port = soc.getsockname()
    return port

  def __read_data(self):
    while True:
      try:
        message, _ = self.soc.recvfrom(4096)
        if not self.connected:
          self.coordinator.notify("connection")
          self.connected = True
          self.soc.settimeout(MESSAGE_TIMEOUT)
        data_snapshot = self.parser.parse_telemetry_message(message)
        self.coordinator.notify("snapshot", data_snapshot)
      except:
        self.coordinator.notify("disconnection")
        break
