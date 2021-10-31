# Copyright Schulich Racing FSAE
# Written By Justin Tijunelis

from main import app
from flask import request
from session_coordinator import SessionCoordinator

class SessionDispatcher:
  def __init__(self):
    self.session_coordinators = {}
    pass

  @app.route('/iot/<serial_number:serial_number>/start', methods=['POST'])
  def start_session(self, serial_number):
    new_session = SessionCoordinator(serial_number, request.remote_addr)
    self.session_coordinators[serial_number] = new_session
    pass

  def stop_session(self, serial_number):
    del self.session_coordinators[serial_number]
    pass