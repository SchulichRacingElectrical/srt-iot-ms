# Copyright Schulich Racing FSAE
# Written By Justin Tijunelis

from flask import request
from iot.main import app
from iot.session_coordinator import SessionCoordinator

class SessionDispatcher:
  def __init__(self):
    self.session_coordinators = {}

  @app.route('/iot/<serial_number:serial_number>/start', methods=['POST'])
  def start_session(self, serial_number):
    new_session = SessionCoordinator(serial_number, request.remote_addr)
    self.session_coordinators[serial_number] = new_session
    return ... # What does the hardware need back?

  def stop_session(self, serial_number):
    self.session_coordinators.pop(serial_number)
    # TODO: Make a publisher acknowledgement