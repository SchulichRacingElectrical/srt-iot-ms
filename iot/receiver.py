# Copyright Schulich Racing FSAE
# Written By Justin Tijunelis, Camilla Abdrazakov, Jonathan Mulyk

import sys
import socket
import threading
import time
from parser import Parser

"""
UDP variable frequency data receiver from telemetry hardware. 
"""
class Receiver:
  def __init__(self, sensors):
    self.sensors = sensors
    self.last_packet_time = -1
    self.parser = Parser(self.sensors)

  def start_receiver(self, port) -> None:
    soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
      soc.bind(('', port))
    except socket.error as msg:
      print("Bind failed. Error: " + str(sys.exc_info()))
    packet_resetter = threading.Thread(target = self.__handle_disconnect)
    packet_resetter.start()
    self.__read_data(soc)

  def __read_data(self, sock) -> None:
    while True:
      message, _ = sock.recvfrom(4096)
      self.last_packet_time = int(round(time.time() * 1000))
      data = self.parser.parse_telemetry_message(message)
      # TODO: Handle data

  def __handle_disconnect(self) -> None:
    while True:
      time.sleep(1)
      current_time = int(round(time.time() * 1000))
      delta = current_time - self.last_packet_time 
      if (self.last_packet_time != -1 and delta > 1000): # TODO: Have timeout for now data coming
        pass
        # There was a disconnection
        # TODO: Send a message indicating this and delete this object
        # TODO: Need a timeout for never receiving data
