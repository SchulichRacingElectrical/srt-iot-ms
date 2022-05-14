# Copyright Schulich Racing FSAE
# Written By Justin Tijunelis

from ..session.sensors import SessionSensors
from ..session.receiver import SessionReceiver
from ..session.transmitter import SessionTransmitter
from ..session.emitter import SessionEmitter
from ..redis.publisher import publisher

class SessionCoordinator:
  def __init__(self, api_key, thing_id, hw_address):
    self.api_key = api_key
    self.thing_id = thing_id
    self.transmitter = SessionTransmitter(hw_address)

  def start_receiver(self):
    sensors = Sensors(api_key, thing_id)
    if not sensors.fetch_sensors():
      return -1
    else:
      # TODO: Create socket-io connection with gateway
      self.emitter = SessionEmitter()
      self.receiver = SessionReceiver(sensors, self)
      return self.receiver.start()

  def notify(self, message, data = {}):
    publisher.publish_message(message, self.api_key, self.thing_id, data)
    if message == ("disconnection" or "error"):
      self.receiver.stop()
