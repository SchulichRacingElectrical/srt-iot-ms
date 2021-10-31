# Copyright Schulich Racing FSAE
# Written By Justin Tijunelis

from main import app
from sensors import Sensors
from receiver import Receiver

class SessionCoordinator:
  def __init__(self, serial_number, hw_address):
    self.serial_number = serial_number
    # TODO: Create receiver, transmitter, and set up publisher?

  @app.route('/iot/{self.serial_number}/sensors', methods=['GET'])
  def get_sensors(self, last_retrieved_time):
    # TODO: Create the sensor diff
    return ... # Nothing or a list of updated sensors

  def fetch_sensors(self):
    # TODO: Create sensors class and fetch all of the sensor data
    pass