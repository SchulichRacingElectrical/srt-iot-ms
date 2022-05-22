# Copyright Schulich Racing FSAE
# Written By Justin Tijunelis

from iot.session.receiver import SessionReceiver
from iot.session.thing import SessionThing


class SessionCoordinator:
    def __init__(self, hw_address):
        self.hw_address = hw_address
        # self.transmitter = SessionTransmitter(hw_address)

    def start_receiver(self, key, thing_id, close_callback):
        thing = SessionThing(key, thing_id)
        if thing.fetch_sensors():
            self.receiver = SessionReceiver(thing, close_callback)
            port = self.receiver.start()
            return port if port > 0 else -1
        else:
            return -1

    def stop(self):
        # TODO: Transmit to hardware to stop
        return False
