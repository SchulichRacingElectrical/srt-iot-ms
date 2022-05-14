# Copyright Schulich Racing FSAE
# Written By Justin Tijunelis

from flask import Flask, request, jsonify
from iot.session.dispatcher import SessionDispatcher
from iot.session.coordinator import SessionCoordinator
from dotenv import load_dotenv
load_dotenv()

# Global Variables
app = Flask(__name__)
dispatcher = SessionDispatcher()

"""
Used by hardware to start a session for the hardware. Spawns a session coordinator
that will handle incoming data from the IoT device. 
"""
@app.route('/<string:serial_number>/start', methods=['GET'])
def start_session(serial_number):
  key = request.headers.get('apiKey')
  new_session = SessionCoordinator(key, serial_number, request.remote_addr)
  dispatcher.session_coordinators[serial_number] = new_session
  udp_port = new_session.start_receiver()
  if udp_port > 0: return jsonify({"port": udp_port, "address": "127.0.0.1"}) # TODO: Get public ip address
  else: return "Could not start session.", 500

"""
Used to transmit reliable messages to the hardware for display messages
or requests to start/stop telemetry. Message format must be in the format 
[CODE, MESSAGE], where the code is 0-9, and the message contains no additional
commas. 
"""
@app.route('/real-time/<string:serial_number>/message', methods=['POST'])
def send_message(serial_number):
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

@app.route('/real-time/<string:serial_number>/sensor/<string:sensor_id>/data', methods=['GET'])
def fetch_real_time_sensor_data(serial_number, sensor_id):
  # Read data from redis and return
  pass

# TODO: Only allow traffic from local host via node js server

# Starting the server
if __name__ == "__main__":  
  app.run()
