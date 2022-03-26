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
# TODO: Connection timeout of some sort (Timeout for idle)
class Receiver:
  def __init__(self, sensors, coordinator):
    self.sensors = sensors
    self.coordinator = coordinator
    self.last_packet_time = -1
    self.parser = Parser(self.sensors)

  def start_receiver(self, port):
    soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
      soc.bind(('', port))
    except socket.error as msg:
      print("Bind failed. Error: " + str(sys.exc_info()))
      self.coordinator.notify("error")
<<<<<<< Updated upstream
    packet_resetter = threading.Thread(target = self.__handle_disconnect)
    packet_resetter.start()
    self.__read_data(soc)

  def __read_data(self, sock):
    while True:
      message, _ = sock.recvfrom(4096)
      if self.last_packet_time == -1:
        self.coordinator.notify("connection")
      self.last_packet_time = int(round(time.time() * 1000))
      data_snapshot = self.parser.parse_telemetry_message(message)
      self.coordinator.notify("snapshot", data_snapshot)
=======
      return -1
    self.udp_listener = threading.Thread(target = self.__read_data)
    self.udp_listener.start()
    _, port = self.soc.getsockname()
    return port
>>>>>>> Stashed changes

  def __handle_disconnect(self):
    while True:
      time.sleep(1)
      current_time = int(round(time.time() * 1000))
      delta = current_time - self.last_packet_time 
      if self.last_packet_time != -1 and delta > 1000: 
        self.coordinator.notify("disconnection")
