# Copyright Schulich Racing FSAE
# Written By Justin Tijunelis

from iot.auth import require_api_key
from iot.session_coordinator import SessionCoordinator
from flask import request
import json

class SessionDispatcher:
  def __init__(self):
    self.session_coordinators = {}

  def stop_session(self, thing_id):
    self.session_coordinators[thing_id].notify("disconnection", "")
    self.session_coordinators.pop(thing_id)