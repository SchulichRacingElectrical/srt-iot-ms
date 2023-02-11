# Copyright Schulich Racing FSAE
# Written By Justin Tijunelis

from typing import Callable

from iot.session.receiver import SessionReceiver
from iot.session.thing import SessionThing


class SessionCoordinator:
    def __init__(self, hw_address: str):
        self.hw_address = hw_address
        # self.transmitter = SessionTransmitter(hw_address)

    def start_receiver(self, key: str, thing_id: str, close_callback: Callable):
        thing = SessionThing(key, thing_id)
        if thing.fetch_sensors():
            self.receiver = SessionReceiver(thing, close_callback)
            return self.receiver.start()

    def stop(self):
        # TODO: Transmit to hardware to stop
        return False
