# Copyright Schulich Racing FSAE
# Written By Justin Tijunelis

from dotenv import load_dotenv
load_dotenv()

from flask import Flask
from iot.publisher import Publisher
from iot.session_dispatcher import SessionDispatcher

app = Flask(__name__)

if __name__ == "__main__":
  # Create the redis publisher
  publisher = Publisher()
  
  # Create the session dispatcher
  dispatcher = SessionDispatcher()

  # Start the HTTP server
  app.run()
