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
    sensors = SessionSensors(self.api_key, self.thing_id)
    if not sensors.fetch_sensors():
      return -1
    else:
      self.receiver = SessionReceiver(sensors, self)
      port = self.receiver.start()
      if port > 0:
        self.emitter = SessionEmitter(self.thing_id)
        self.emitter.start()
        return port
      else: return -1

  def notify(self, message, data = {}):
    publisher.publish_message(message, self.api_key, self.thing_id, data)
    if message == ("disconnection" or "error"):
      self.receiver.stop()
      self.emitter.stop()
    elif message == "snapshot":
      self.emitter.emit_data(data)
