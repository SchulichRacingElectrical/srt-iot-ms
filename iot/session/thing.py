# Copyright Schulich Racing FSAE
# Written By Justin Tijunelis

import os

import requests


class SessionThing:
    def __init__(self, api_key: str, thing_id: str):
        self.api_key = api_key
        self.thing_id = thing_id
        self.sensor_list = {}

    def fetch_sensors(self):
        gateway_route = os.getenv("GATEWAY_ROUTE")
        if gateway_route is None:
            return False

        url = gateway_route + "/api/database/sensors/thing/" + self.thing_id
        headers = {"Accept": "application/json", "apiKey": self.api_key}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            self.sensor_list = response.json()["data"]
        return response.status_code == 200

    def get_sensor_type(self, small_id: str):
        sensors = list(filter(lambda s: s["smallId"] == small_id, self.sensor_list))
        return sensors[0]["type"] if len(sensors) != 0 else ""

    def get_transmission_frequency(self):
        highest_frequency = 0
        for sensor in self.sensor_list:
            if sensor["frequency"] > highest_frequency:
                highest_frequency = sensor["frequency"]
        return highest_frequency
