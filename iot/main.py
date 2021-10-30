# Copyright Schulich Racing FSAE
# Written By Justin Tijunelis

from flask import Flask
from receiver import Receiver
from sensors import Sensors
from relay import Relay
from transmitter import Transmitter

app = Flask(__name__)

if __name__ == "__main__":
  # Initialize sensor information
  sensors = Sensors()

  # Create a relay server
  relay = Relay(sensors=sensors)
  
  # Start the receiver
  # TODO: This server should be able to handle data from multiple sources
  receiver = Receiver(sensors=sensors, relay=relay)
  receiver.start_receiver(4500)

  # Start the transmitter (to hardware)
  transmitter = Transmitter(sensors=sensors)

  # Start the TCP server
  app.run()
