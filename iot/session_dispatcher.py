# Copyright Schulich Racing FSAE
# Written By Justin Tijunelis

from flask import request, Flask
app = Flask(__name__) # Check this
from iot.auth import require_api_key
from iot.session_coordinator import SessionCoordinator
import json

class SessionDispatcher:
  def __init__(self):
    self.session_coordinators = {}

  @app.route('/iot/<string:serial_number>/start', methods=['POST'])
  @require_api_key
  def start_session(self, key, serial_number):
    new_session = SessionCoordinator(self, key, serial_number, request.remote_addr)
    self.session_coordinators[serial_number] = new_session
    udp_port = new_session.start_receiver()
    if udp_port > 0:
      return json.stringify({"port": udp_port})
    else:
      return 500 # Don't think this is right?

  def stop_session(self, serial_number):
    self.session_coordinators.pop(serial_number)