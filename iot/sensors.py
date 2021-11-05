# Copyright Schulich Racing FSAE
# Written By Justin Tijunelis

import os
import requests
from requests.auth import HTTPBasicAuth

class Sensors:
  def __init__(self, api_key):
    self.api_key = api_key
    self.sensor_list = []
    self.__fetch_sensors()

  def __fetch_sensors(self):
    url = os.getenv('GATEWAY_ROUTE')
    headers = {'Accept': 'application/json'}
    auth = HTTPBasicAuth('apikey', self.api_key)
    response = requests.get(url, headers=headers, auth=auth)
    if response.status_code == 200:
      self.sensor_list = response.json()

  def get_data_snapshot(self, data, sensor_ids):
    snapshot_sensors = []
    for i, sensor_id in enumerate(sensor_ids):
      snapshot = {}
      snapshot[sensor_id] = data[i]
      snapshot_sensors.append(snapshot)
    return snapshot_sensors

  def get_sensor_type(self, sensor_id):
    sensor = filter(lambda s: s.sensor_id == sensor_id, self.sensor_list)
    return sensor.type