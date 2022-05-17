# Copyright Schulich Racing FSAE
# Written By Justin Tijunelis

from flask import Flask, request, jsonify
from iot.session.dispatcher import SessionDispatcher
from iot.session.coordinator import SessionCoordinator
from iot.redis.reader import reader
from dotenv import load_dotenv
load_dotenv()

# Global Variables
app = Flask(__name__)
dispatcher = SessionDispatcher()

"""
Used by hardware to start a session for the hardware. Spawns a session coordinator
that will handle incoming data from the IoT device. 
"""
@app.route('/<string:thing_id>/start', methods=['GET'])
def start_session(thing_id):
  key = request.headers.get('apiKey') # TODO: Check that this is here
  port = dispatcher.start_session(key, thing_id, request.remote_addr)
  if port > 0: 
    # TODO: Get public ip address
    return jsonify({"port": udp_port, "address": "127.0.0.1"}) 
  else: 
    return "Could not start session.", 500

"""
Used to transmit reliable messages to the hardware for display messages
or requests to start/stop telemetry. Message format must be in the format 
[CODE, MESSAGE], where the code is 0-9, and the message contains no additional
commas. 
"""
@app.route('/real-time/<string:thing_id>/message', methods=['POST'])
def send_message(thing_id):
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

"""
TODO
"""
@app.route('/real-time/<string:thing_id>/data', methods=['GET', 'POST'])
def fetch_real_time_thing_data(thing_id):
  # TODO: Check request type
  # Read sensor ids?
  try:
    data = reader.fetch_thing_data(thing_id)
    return jsonify({data: data, message: "Success!"})
  except:
    return "", 500 # Say if redis error or thing not streaming

"""

"""
@app.route('/real-time/<string:thing_id>/sensor/<string:sensor_id>/data', methods=['GET'])
def fetch_real_time_sensor_data(thing_id, sensor_id):
  # TODO
  try:
    data = reader.fetch_sensor_data(thing_id, sensor_ids)
    return jsonify({data: data, message: "Hurray"})
  except:
    return "", 500 # Say if redis error or thing not streaming


# TODO: Only allow traffic from local host via node js server

# Starting the server
if __name__ == "__main__":  
  app.run()
