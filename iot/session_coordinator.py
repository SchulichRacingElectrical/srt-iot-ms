# Copyright Schulich Racing FSAE
# Written By Justin Tijunelis

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
