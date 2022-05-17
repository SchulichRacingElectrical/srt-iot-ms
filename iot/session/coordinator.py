# Copyright Schulich Racing FSAE
# Written By Justin Tijunelis

from ..session.thing import SessionThing
from ..session.receiver import SessionReceiver
from ..session.transmitter import SessionTransmitter
import asyncio

class SessionCoordinator:
  def __init__(self, hw_address):
    self.hw_address = hw_address
    # self.transmitter = SessionTransmitter(hw_address)

  def start_receiver(self, key, thing_id):
    thing = SessionThing(key, thing_id)
    if thing.fetch_sensors():
      self.receiver = SessionReceiver(thing)
      port = self.receiver.start()
      return port if port > 0 else -1
    else:
      return -1

  def stop(self):
    # TODO: Transmit to hardware to stop
    return False
