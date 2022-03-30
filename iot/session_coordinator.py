# Copyright Schulich Racing FSAE
# Written By Justin Tijunelis

from iot.sensors import Sensors
from iot.receiver import Receiver
from iot.transmitter import Transmitter
from iot.auth import require_api_key
from iot.publisher import publisher
import json

class SessionCoordinator:
  def __init__(self, api_key, thing_id, hw_address):
    self.api_key = api_key
    self.thing_id = thing_id
    self.receiver = Receiver(Sensors(api_key, thing_id), self)
    self.transmitter = Transmitter(hw_address)

  def start_receiver(self):
    return self.receiver.start()

  def notify(self, message, data):
    publisher.publish_message(message, self.api_key, self.thing_id, data)
    if message == ("disconnection" | "error"):
      self.receiver.stop()
