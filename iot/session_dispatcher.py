# Copyright Schulich Racing FSAE
# Written By Justin Tijunelis

from flask import request
from main import app
from session_coordinator import SessionCoordinator
from auth import require_api_key

class SessionDispatcher:
  def __init__(self):
    self.session_coordinators = {}

  @app.route('/iot/<string:serial_number>/start', methods=['POST'])
  @require_api_key
  def start_session(self, key, serial_number):
    # TODO: Get API key
    new_session = SessionCoordinator(serial_number, request.remote_addr)
    self.session_coordinators[serial_number] = new_session
    return 200 

  def stop_session(self, serial_number):
    self.session_coordinators.pop(serial_number)
    # TODO: Make a publisher acknowledgement