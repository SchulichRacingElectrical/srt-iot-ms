# Copyright Schulich Racing FSAE
# Written By Justin Tijunelis

from flask import Flask, request
from iot.session_dispatcher import SessionDispatcher
from iot.session_coordinator import SessionCoordinator
from iot.auth import require_api_key
from dotenv import load_dotenv
import json
load_dotenv()

# Global Variables
app = Flask(__name__)
dispatcher = SessionDispatcher()

"""
Used by hardware to start a session for the hardware. Spawns a session coordinator
that will handle incoming data from the IoT device. 
"""
@app.route('/iot/<string:thing_id>/start', methods=['POST'])
@require_api_key
def start_session(key, thing_id):
  new_session = SessionCoordinator(key, thing_id, request.remote_addr)
  dispatcher.session_coordinators[thing_id] = new_session
  udp_port = new_session.start_receiver()
  return json.stringify({"port": udp_port}) if udp_port > 0 else "Could not start session.", 500

"""
Used to transmit reliable messages to the hardware for display messages
or requests to start/stop telemetry. Message format must be in the format 
[CODE, MESSAGE], where the code is 0-9, and the message contains no additional
commas. 
"""
@app.route('/iot/<string:serial_number>/message', methods=['GET'])
@require_jwt
def send_message(key, thing_id):
  if request.is_json:
    try:
      message = request.json['message']
      success = dispatcher.session_coordinators[thing_id].transmitter.transmit_message(message)
      if success and message == "0,stop":
        dispatcher.stop_session(thing_id)
      return "", 200 if success else "", 500
    except:
      return "", 500
  else:
    return "", 400

# Starting the server
if __name__ == "__main__":  
  app.run()
