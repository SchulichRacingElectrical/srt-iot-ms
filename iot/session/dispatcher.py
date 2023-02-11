# Copyright Schulich Racing FSAE
# Written By Justin Tijunelis

from iot.session.coordinator import SessionCoordinator


class SessionDispatcher:
    def __init__(self):
        self.session_coordinators = {}

    def start_session(self, key: str, thing_id: str, hw_address: str):
        new_session = SessionCoordinator(hw_address)
        udp_port = new_session.start_receiver(
            key, thing_id, self.delete_session
        )  # Make sure this supports ipv6
        if udp_port is not None:
            self.session_coordinators[thing_id] = new_session
        return udp_port

    def stop_session(self, thing_id: str):
        if thing_id in self.session_coordinators:
            self.session_coordinators[thing_id].stop()
            del self.session_coordinators[thing_id]

    def delete_session(self, thing_id: str):
        if thing_id in self.session_coordinators:
            del self.session_coordinators[thing_id]
