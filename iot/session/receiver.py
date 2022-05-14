# Copyright Schulich Racing FSAE
# Written By Justin Tijunelis, Camilla Abdrazakov, Jonathan Mulyk

import sys
import socket
import threading
import time
from ..utils.parser import Parser

CONNECTION_TIMEOUT = 10.0
MESSAGE_TIMEOUT = 3.0

"""
UDP variable frequency data receiver from telemetry hardware. 
"""
class SessionReceiver:
  def __init__(self, sensors, coordinator):
    self.coordinator = coordinator
    self.connected = False
    self.stopping = False
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
    _, port = self.soc.getsockname()
    return port

  def stop(self):
    self.stopping = True
    self.soc.settimeout(0.0001)

  def __read_data(self):
    while True:
      try:
        message, _ = self.soc.recvfrom(4096)
        if self.stopping:
          return
        if not self.connected:
          self.coordinator.notify("connection")
          self.connected = True
          self.soc.settimeout(MESSAGE_TIMEOUT)
        if len(message) < 6:
          continue
        data_snapshot = self.parser.parse_telemetry_message(message)
        if data_snapshot == {}:
          continue
        self.coordinator.notify("snapshot", data_snapshot)
      except:
        if not self.stopping:
          self.coordinator.notify("disconnection")
        return
