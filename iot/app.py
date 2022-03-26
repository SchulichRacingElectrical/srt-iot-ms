# Copyright Schulich Racing FSAE
# Written By Justin Tijunelis

from flask import Flask
app = Flask(__name__)
from iot.session_dispatcher import SessionDispatcher
from iot.auth import require_api_key
from dotenv import load_dotenv
load_dotenv()

# Global Variables
dispatcher = SessionDispatcher()

# Endpoints
@app.route('/iot/<string:serial_number>/start')
@require_api_key
def start_session(key, serial_number):
  new_session = SessionCoordinator(dispatcher, key, serial_number, request.remote_addr)
  dispatcher.session_coordinators[serial_number] = new_session
  udp_port = new_session.start_receiver()
  if udp_port > 0:
    return json.stringify({"port": udp_port})
  else:
    return 500 # Don't think this is right?

@app.route('/iot/<string:serial_number>/stop')
@require_api_key
def stop_session(key, serial_number):
  pass

@app.route('/iot/<string:serial_number>/sensors')
@require_api_key
def get_sensors(key, serial_number, last_retrieved_time):
  #   diff = self.sensors.get_sensor_diff(last_retrieved_time)
  #   return json.stringify(diff)
  pass

@app.route('/iot/<string:serial_number>/sensor_diff')
@require_api_key
def get_sensor_diff(key, serial_number):
  pass

@app.route('/iot/<string:serial_number>/message')
@require_api_key
def send_message(key, serial_number):
  #   if request.is_json:
  #     try:
  #       success = self.transmitter.transmit_message(request.json['message'])
  #       return 200 if success else 500
  #     except:
  #       return 500
  #   else: 
  #     return 400
  pass

if __name__ == "__main__":  
  # Start the HTTP server
  app.run()
