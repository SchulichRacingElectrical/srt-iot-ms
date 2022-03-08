# Copyright Schulich Racing FSAE
# Written By Justin Tijunelis, Camilla Abdrazakov, Jonathan Mulyk

import struct

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
    # Double check if big or little endian
    timestamp = int.from_bytes(message.decode()[1:sensor_count + 1], "big", signed = False)
    sensor_ids = list(message.decode()[5:sensor_count + 1])
    data_format = self.get_data_format(sensor_ids)
    data = struct.unpack(data_format, message[sensor_count + 5:])
    data_snapshot = []
    for i, sensor_id in enumerate(sensor_ids):
      snapshot = {}
      snapshot[sensor_id] = data[i]
      data_snapshot.append(snapshot)
    return data_snapshot

  def get_data_format(self, sensor_ids):
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