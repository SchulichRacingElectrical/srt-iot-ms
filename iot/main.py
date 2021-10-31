# Copyright Schulich Racing FSAE
# Written By Justin Tijunelis

from flask import Flask
from receiver import Receiver
from sensors import Sensors
from transmitter import Transmitter

app = Flask(__name__)

if __name__ == "__main__":
  # Start the HTTP server
  app.run()
