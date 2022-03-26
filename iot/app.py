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

# Endpoints
@app.route('/iot/<string:serial_number>/start', methods=['POST'])
@require_api_key
def start_session(key, serial_number):
  new_session = SessionCoordinator(dispatcher, key, serial_number, request.remote_addr)
  dispatcher.session_coordinators[serial_number] = new_session
  udp_port = new_session.start_receiver()
  if udp_port > 0:
    return json.stringify({"port": udp_port})
  else:
    return "Could not start session.", 500

@app.route('/iot/<string:serial_number>/stop', methods=['POST'])
@require_api_key
def stop_session(key, serial_number):
  # Send message to the car to shut down the logging
  # Shut down the coordinator
  # Return a message indicating success
  pass

@app.route('/iot/<string:serial_number>/sensors', methods=['GET'])
@require_api_key
def get_sensors(key, serial_number, last_retrieved_time):
  sensors = dispatcher.session_coordinators[serial_number].sensors.fetch_sensors()
  return json.stringify(sensors)

@app.route('/iot/<string:serial_number>/sensor_diff', methods=['GET'])
@require_api_key
def get_sensor_diff(key, serial_number):
  diff = dispatcher.session_coordinators[serial_number].sensors.get_sensor_diff()
  return json.stringify(diff)

@app.route('/iot/<string:serial_number>/message', methods=['GET'])
@require_api_key
def send_message(key, serial_number):
  if request.is_json:
    try:
      success = dispatcher.session_coordinators[serial_number].transmitter.transmit_message(request.json['message'])
      return "", 200 if success else "", 500
    except:
      return "", 500
  else:
    return "", 400

# Starting the server
if __name__ == "__main__":  
  app.run()
