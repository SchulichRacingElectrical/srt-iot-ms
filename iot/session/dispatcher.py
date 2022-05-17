# Copyright Schulich Racing FSAE
# Written By Justin Tijunelis

from ..session.coordinator import SessionCoordinator

class SessionDispatcher:
  def __init__(self):
    self.session_coordinators = {}

  def start_session(self, key, thing_id, hw_address):
    new_session = SessionCoordinator(hw_address)
    udp_port = new_session.start_receiver(key, serial_number) # Make sure this supports ipv6
    if udp_port > 0:
      self.session_coordinators[serial_number] = new_session
    return udp_port

  def stop_session(self, thing_id):
    self.session_coordinators[thing_id].stop()
    del self.session_coordinators[thing_id]

  def delete_session(self, thing_id):
    del self.session_coordinators[thing_id]