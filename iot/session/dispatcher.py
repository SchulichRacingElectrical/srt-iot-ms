# Copyright Schulich Racing FSAE
# Written By Justin Tijunelis

from ..session.coordinator import SessionCoordinator

class SessionDispatcher:
  def __init__(self):
    self.session_coordinators = {}

  def stop_session(self, thing_id):
    self.session_coordinators[thing_id].notify("disconnection", "")
    self.session_coordinators.pop(thing_id)