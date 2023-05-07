# Copyright Schulich Racing FSAE
# Written By Justin Tijunelis

import os

from dotenv import load_dotenv
from flask import Flask, jsonify, request
from iot.redis_handler.reader import reader
from iot.session.dispatcher import SessionDispatcher

load_dotenv()

# Global Variables
app = Flask(__name__)
dispatcher = SessionDispatcher()


@app.route("/", methods=["GET"])
def index():
    return os.getenv("IPV4")


# TODO: Take last update timestamp as query parameter, and return updated sensor data from that time
@app.route("/<string:thing_id>/start", methods=["GET"])
def start_session(thing_id: str):
    """
    Used by hardware to start a session for the hardware. Spawns a session coordinator
    that will handle incoming data from the IoT device.
    """
    key = request.headers.get("apiKey")
    if not key:
        return "Not authorized.", 401
    if not request.remote_addr:
        return "Could not get remote address.", 500

    port = dispatcher.start_session(key, thing_id, request.remote_addr)
    if port is None:
        return "Could not start session.", 500

    # data = json.loads(urllib.request.urlopen("http://ip.jsontest.com/").read()) FUTURE, puts out an ipv6 port
    # TODO: Add timestamp and sensor updates
    return jsonify({"port": port, "address": os.getenv("IPV4")})


@app.route("/real-time/<string:thing_id>/message", methods=["POST"])
def send_message(thing_id: str):
    """
    Used to transmit reliable messages to the hardware for display messages
    or requests to start/stop telemetry. Message format must be in the format
    [CODE, MESSAGE], where the code is 0-9, and the message contains no additional
    commas.
    """
    if request.is_json and request.json:
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


@app.route("/real-time/<string:thing_id>/data", methods=["GET"])
def fetch_real_time_thing_data(thing_id):
    """
    Fetches data that the client may be missing
    """
    try:
        data = reader.fetch_thing_data(thing_id)
        if data == None:
            return "", 404
        return jsonify({"data": data, "message": "Success!"})
    except:
        return "", 500


# TODO: Only allow traffic from local host via node js server

# Starting the server
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8001, debug=True)
