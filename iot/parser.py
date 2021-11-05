# Copyright Schulich Racing FSAE
# Written By Justin Tijunelis, Camilla Abdrazakov, Jonathan Mulyk

import struct
import ctypes

sensor_types = {
  'q': 8,           # long long
  'd': 8,           # double
  'f': 4,           # float
  'i': 4,           # integer
  'h': 2,           # short
  'e': 2,           # short float
  'c': 1,           # char
  '?': 1,           # bool
}

"""

"""
class Parser:
  def __init__(self, sensors):
    self.sensors = sensors

  def parse_telemetry_message(self, message):
    sensor_count = message[0]
    sensor_ids = list(message.decode()[1:sensor_count + 1])
    data_format = get_data_format(sensor_ids)
    data = struct.unpack(data_format, message[sensor_count + 1:])
    data_snapshot = self.sensors.get_data_snapshot(data, sensor_ids)
    return data_snapshot

  def get_data_format(self, sensor_ids):
    # TODO: Handle case where key is invalid
    data_format = ""
    running_count = 0
    for i, sensor_id in enumerate(sensor_ids):
      data_type = self.sensors.get_sensor_type(sensor_id)
      data_size = sensor_types[data_type]
      data_format += data_type
      running_count += data_size
      if running_count % 4 != 0:
        remaining_bytes_in_word = 4 - (running_count % 4)
        if i == len(sensor_ids) - 1:
          data_format += 'x' * remaining_bytes_in_word
          running_count += remaining_bytes_in_word
        else:
          next_id = sensor_ids[i + 1]
          next_type = self.sensors.get_sensor_type(next_id)
          next_size = sensor_types[next_type]
          if next_size > remaining_bytes_in_word:
            data_format += 'x' * remaining_bytes_in_word
            running_count += remaining_bytes_in_word
    return "<" + data_format if data_format != "" else data_format