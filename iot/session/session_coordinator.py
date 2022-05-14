# Copyright Schulich Racing FSAE
# Written By Justin Tijunelis

from ..session.sensors import Sensors
from ..session.receiver import Receiver
from ..session.transmitter import Transmitter
from ..redis.publisher import publisher

class SessionCoordinator:
  def __init__(self, api_key, thing_id, hw_address):
    self.api_key = api_key
    self.thing_id = thing_id
    self.transmitter = Transmitter(hw_address)

  def start_receiver(self):
    sensors = Sensors(api_key, thing_id)
    if not sensors.fetch_sensors():
      return -1
    else:
      self.receiver = Receiver(sensors, self)
      return self.receiver.start()

  def notify(self, message, data = {}):
    publisher.publish_message(message, self.api_key, self.thing_id, data)
    if message == ("disconnection" or "error"):
      self.receiver.stop()
