# Copyright Schulich Racing FSAE
# Written By Justin Tijunelis

import os
import requests
from requests.auth import HTTPBasicAuth

class Sensors:
  def __init__(self, api_key, serial_number):
    self.api_key = api_key
    self.serial_number = serial_number
    self.sensor_list = []
    self.__fetch_sensors()

  def __fetch_sensors(self):
    url = os.getenv('GATEWAY_ROUTE')
    headers = {'Accept': 'application/json'}
    auth = HTTPBasicAuth('apikey', self.api_key)
    response = requests.get(url + serial_number, headers=headers, auth=auth)
    if response.status_code == 200:
      self.sensor_list = response.json()

  def get_sensor_type(self, sensor_id):
    sensor = filter(lambda s: s.sensor_id == sensor_id, self.sensor_list)
    return sensor.type