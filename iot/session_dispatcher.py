# Copyright Schulich Racing FSAE
# Written By Justin Tijunelis

# from iot.app import app
from iot.auth import require_api_key
from iot.session_coordinator import SessionCoordinator
from flask import request
import json

class SessionDispatcher:
  def __init__(self):
    self.session_coordinators = {}

  def stop_session(self, serial_number):
    self.session_coordinators.pop(serial_number)