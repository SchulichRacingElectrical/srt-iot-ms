# Copyright Schulich Racing FSAE
# Written By Justin Tijunelis

import os
import requests
from requests.auth import HTTPBasicAuth

class Sensors:
  def __init__(self, api_key, thing_id):
    self.api_key = api_key
    self.thing_id = thing_id
    self.sensor_list = []
    self.fetch_sensors()

  def fetch_sensors(self):
    url = os.getenv('GATEWAY_ROUTE') + "/database/sensors/" + self.thing_id
    headers = {'Accept': 'application/json', 'apiKey': self.api_key}
    response = requests.get(url + self.thing_id, headers=headers, auth=auth)
    if response.status_code == 200:
      self.sensor_list = response.json() # Convert to dict?
    return response.status_code == 200

  def get_sensor_type(self, small_id):
    sensors = list(filter(lambda s: s['smallId'] == small_id, self.sensor_list))
    return sensors[0]['type'] if len(sensors) != 0 else ""

  # Just for unit testing right now
  def set_sensor_list(self, sensor_list):
    self.sensor_list = sensor_list
    