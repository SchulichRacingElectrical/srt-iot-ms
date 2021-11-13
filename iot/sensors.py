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

  def fetch_sensors(self):
    """
    Requests the sensor list from the database microservice.
    This function will automatically set the sensor list on a successful retrieval.
    The array form of the sensor list will be returned. 
    """
    url = os.getenv('GATEWAY_ROUTE')
    headers = {'Accept': 'application/json'}
    auth = HTTPBasicAuth('apikey', self.api_key)
    response = requests.get(url + self.serial_number, headers=headers, auth=auth)
    if response.status_code == 200:
      self.sensor_list = response.json()
      return self.sensor_list
    else:
      return []

  def set_sensor_list(self, sensor_list):
    self.sensor_list = sensor_list

  def get_sensor_type(self, sensor_id):
    sensors = list(filter(lambda s: s['sensor_id'] == sensor_id, self.sensor_list))
    return sensors[0]['type'] if len(sensors) != 0 else ""

  def get_sensor_diff(self, date):
    # TODO: Find the changed sensors, compress to byte format
    return ...
    