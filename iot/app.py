# Copyright Schulich Racing FSAE
# Written By Justin Tijunelis

import json
import urllib.request
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from iot.redis.reader import reader
from iot.session.dispatcher import SessionDispatcher

load_dotenv()

# Global Variables
app = Flask(__name__)
dispatcher = SessionDispatcher()

"""
Used by hardware to start a session for the hardware. Spawns a session coordinator
that will handle incoming data from the IoT device. 
"""
@app.route("/<string:thing_id>/start", methods=["GET"])
def start_session(thing_id):
    key = request.headers.get("apiKey")
    if not key:
        return "Not authorized.", 401
    port = dispatcher.start_session(key, thing_id, request.remote_addr)
    if port > 0:
        data = json.loads(urllib.request.urlopen("http://ip.jsontest.com/").read())
        # data["ip"]
        return jsonify({"port": port, "address": "127.0.0.1"})
    else:
        return "Could not start session.", 500

"""
Used to transmit reliable messages to the hardware for display messages
or requests to start/stop telemetry. Message format must be in the format 
[CODE, MESSAGE], where the code is 0-9, and the message contains no additional
commas. 
"""
@app.route("/real-time/<string:thing_id>/message", methods=["POST"])
def send_message(thing_id):
    if request.is_json:
        try:
            message = request.json["message"]
            success = dispatcher.session_coordinators[thing_id].transmitter.transmit_message(
                message
            )
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
@app.route("/real-time/<string:thing_id>/data", methods=["GET"])
def fetch_real_time_thing_data(thing_id):
    try:
        data = reader.fetch_thing_data(thing_id)
        if data == None: return "", 404
        return jsonify({"data": data, "message": "Success!"})
    except:
        return "", 500

# TODO: Only allow traffic from local host via node js server

# Starting the server
if __name__ == "__main__":
    app.run()
