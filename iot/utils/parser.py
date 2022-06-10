# Copyright Schulich Racing FSAE
# Written By Justin Tijunelis, Camilla Abdrazakov, Jonathan Mulyk

import struct

type_size_map = {
    "?": 1,  # bool
    "c": 1,  # char (signed byte)
    "B": 1,  # unsigned byte
    "h": 2,  # short
    "H": 2,  # unsigned short   
    "i": 4,  # integer
    "I": 4,  # unsigned integer
    "f": 4,  # float
    "q": 8,  # long long
    "Q": 8,  # unsigned long long
    "d": 8,  # double
}

class Parser:
    def __init__(self, sensors):
        self.sensors = sensors

    def parse_telemetry_message(self, message):
        # If the message is less than 6 bytes, it must be invalid
        if len(message) < 6:
            return None

        # Ensure there is at least one sensor
        sensor_count = message[0]
        if sensor_count == 0:
            return None

        # Attempt to resolve the data format
        timestamp = int.from_bytes(list(message[1:4]), "little", signed=False)
        sensor_ids = list(message[5:5 + sensor_count])
        data_format = self.get_data_format(sensor_ids)
        if data_format == "":
            return None

        # Attempt to extract the data based on the format
        data = struct.unpack(data_format, message[sensor_count + 5:])
        if len(data) == 0:
            return None

        # Create the data snapshot and return
        data_snapshot = {"ts": timestamp}
        for i, sensor_id in enumerate(sensor_ids):
            data_snapshot[str(sensor_id)] = data[i]
        return data_snapshot

    def get_data_format(self, sensor_ids):
        data_format = ""
        running_count = 0
        for i, sensor_id in enumerate(sensor_ids):
            data_type = self.sensors.get_sensor_type(sensor_id)
            if data_type == "":
                return ""
            data_size = type_size_map[data_type]
            data_format += data_type
            running_count += data_size
        return "<" + data_format if data_format != "" else data_format
