# Copyright Schulich Racing FSAE
# Written By Justin Tijunelis

"""
MQTT communication with telemetry hardware. 
"""
class Transmitter:
  def __init__(self, hw_address):
    self.hw_address = hw_address

  def transmit_message(self):
    pass
    
    