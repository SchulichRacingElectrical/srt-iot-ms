# Copyright Schulich Racing FSAE
# Written By Justin Tijunelis

from iot.main import app
from iot.sensors import Sensors
from iot.receiver import Receiver
from iot.transmitter import Transmitter

class SessionCoordinator:
  def __init__(self, api_key, serial_number, hw_address):
    self.serial_number = serial_number
    self.sensors = Sensors(self.api_key, self.serial_number)
    self.receiver = Receiver(self.sensors)
    self.transmitter = Transmitter(self.hw_address)

  @app.route('/iot/{self.serial_number}/sensors', methods=['GET'])
  def get_sensors(self, last_retrieved_time):
    # TODO: Create the sensor diff
    return ...  # Nothing or a list of updated sensors
    
  @app.route('/iot/{self.serial_number}/message', methods=['POST'])
  def send_message(self):
    # Get request body
    self.transmitter.transmit_message()
