# Copyright Schulich Racing FSAE
# Written By Justin Tijunelis

import struct
import ctypes

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

class Parser:
  def __init__(self, sensors):
    self.sensors = sensors

  def parse_telemetry_message(self, message):
    sensor_count = message[0]
    sensor_ids = list(message.decode()[1:sensor_count + 1])
    data_format = get_data_format(sensor_ids)
    data = struct.unpack(data_format, message[sensor_count + 1:])
    # TODO: Consolidate with sensors
    return data

  def get_data_format(self, sensor_ids):
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