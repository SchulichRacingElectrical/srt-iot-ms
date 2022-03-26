# Copyright Schulich Racing FSAE
# Written By Justin Tijunelis

from flask import Flask
app = Flask(__name__)
from iot.session_dispatcher import SessionDispatcher
from dotenv import load_dotenv
load_dotenv()

if __name__ == "__main__":  
  # Create the session dispatcher
  dispatcher = SessionDispatcher(app)

  # Start the HTTP server
  app.run()
