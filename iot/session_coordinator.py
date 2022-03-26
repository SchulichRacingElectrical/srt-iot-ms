# Copyright Schulich Racing FSAE
# Written By Justin Tijunelis

from iot.app import app
from flask import request
from iot.sensors import Sensors
from iot.receiver import Receiver
from iot.transmitter import Transmitter
from iot.auth import require_api_key
from iot.publisher import Publisher
import json

class SessionCoordinator:
  def __init__(self, dispatcher, api_key, serial_number, hw_address):
    self.dispatcher = dispatcher
    self.api_key = api_key
    self.serial_number = serial_number
    self.sensors = Sensors(api_key, serial_number)
    self.receiver = Receiver(self.sensors, self)
    self.transmitter = Transmitter(hw_address)

  def start_receiver(self):
    return self.receiver.start()

  def notify(self, message, data):
    publisher.publish_message(message, self.api_key, self.serial_number, data)
    if message == ("disconnection" | "error"):
      self.dispatcher.stop_session(self.serial_number)

  @app.route('/iot/{self.serial_number}/sensors', methods=['GET'])
  @require_api_key
  def get_sensors(self, last_retrieved_time):
    diff = self.sensors.get_sensor_diff(last_retrieved_time)
    return json.stringify(diff)
    
  @app.route('/iot/{self.serial_number}/message', methods=['POST'])
  def send_message(self):
    if request.is_json:
      try:
        success = self.transmitter.transmit_message(request.json['message'])
        return 200 if success else 500
      except:
        return 500
    else: 
      return 400
