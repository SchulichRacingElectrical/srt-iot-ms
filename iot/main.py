# Copyright Schulich Racing FSAE
# Written By Justin Tijunelis

from flask import Flask
app = Flask(__name__)
from publisher import *
from session_dispatcher import *
from dotenv import load_dotenv
load_dotenv()

if __name__ == "__main__":
  # Create the redis publisher
  publisher = Publisher()
  
  # Create the session dispatcher
  dispatcher = SessionDispatcher()

  # Start the HTTP server
  app.run()
