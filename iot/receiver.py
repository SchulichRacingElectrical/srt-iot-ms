# Copyright Schulich Racing FSAE
# Written By Justin Tijunelis, Camilla Abdrazakov, Jonathan Mulyk

import sys
import socket
import struct
import ctypes
import threading
import time

# testing
maptypes = {
  'a': 'q',
  'b': 'd',
  'c': 'f',
  'd': 'i',
  'e': 'h',
  'f': 'c',
  'g': '?'
}

sensor_types = {
  'q': 8,           # long long
  'd': 8,           # double
  'f': 4,           # float
  'i': 4,           # integer
  'h': 2,           # short
  'c': 1,           # char
  '?': 1,           # bool
}

"""

"""
class Receiver:
  def __init__(self, sensors, relay):
    self.sensors = sensors
    self.relay = relay
    self.last_packet_time = -1

  def start_receiver(self, port):
    soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
      soc.bind(('', port))
    except socket.error as msg:
      print("Bind failed. Error: " + str(sys.exc_info()))
    packet_resetter = threading.Thread(target = self.__handle_disconnect)
    packet_resetter.start()
    self.read_data(soc)

  def read_data(self, sock):
    self.last_packet_id = -1
    while True:
      # Wait for a new message
      message, _ = sock.recvfrom(4096)
      self.last_packet_time = int(round(time.time() * 1000))

      # Parse the message
      sensor_count = message[0]
      sensor_ids = list(message.decode()[1:sensor_count + 1])

      # Decode the data
      data_format = self.__create_data_format(sensor_ids)
      data = struct.unpack(data_format, message[sensor_count + 1:])
      
      # Handle the data
      if self.last_packet_id < data[0]:
        self.last_packet_id = data[0]
      self.sensors.update_values(data)
      self.relay.send_data()

  def create_data_format(self, sensor_ids):
    data_format = "<"
    running_count = 0
    for i, sensor_id in enumerate(sensor_ids):
      data_type = maptypes[sensor_id]
      data_size = sensor_types[data_type]
      data_format += data_type
      running_count += data_size
      if running_count % 4 != 0:
        remaining_bytes_in_word = 4 - (running_count % 4)
        if i == len(sensor_ids) - 1:
          data_format += 'x' * remaining_bytes_in_word
        else:
          next_data_type = maptypes[sensor_ids[i + 1]]
          next_data_size = sensor_types[next_data_type]
          if next_data_size > remaining_bytes_in_word:
            data_format += 'x' * remaining_bytes_in_word
    return data_format

  def __handle_disconnect(self):
    while True:
      time.sleep(1)
      current_time = int(round(time.time() * 1000))
      if current_time - self.last_packet_time > 1000:
        if self.last_packet_id != -1:
          self.last_packet_id = -1
          # There was a disconnection
          # TODO: Send a message indicating this 
