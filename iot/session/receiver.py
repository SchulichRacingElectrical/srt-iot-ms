# Copyright Schulich Racing FSAE
# Written By Justin Tijunelis, Camilla Abdrazakov, Jonathan Mulyk

import asyncio
import socket
import threading
from typing import Callable

from iot.redis_handler.publisher import RedisPublisher
from iot.redis_handler.reader import reader
from iot.session.emitter import SessionEmitter
from iot.session.thing import SessionThing
from iot.utils.parser import Parser

CONNECTION_TIMEOUT = 30.0
DISCONNECT_TIMEOUT = 10.0
BATCH_SIZE = 25  # Maximum number of elements that can be pushed to Redis at once


class SessionReceiver:
    """
    UDP variable frequency data receiver from telemetry hardware.
    """

    def __init__(self, thing: SessionThing, close_callback: Callable):
        self.thing = thing
        self.close_callback = close_callback
        self.parser = Parser(thing)
        self.emitter = SessionEmitter(thing.api_key, thing.thing_id, thing.sensor_list)
        self.publisher = RedisPublisher(thing.api_key, thing.thing_id)
        self.connected = False
        self.stopping = False

    def start(self):
        try:
            # Attempt to open the socket
            self.soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.soc.bind(("0.0.0.0", 0))
            self.soc.settimeout(CONNECTION_TIMEOUT)

            # Start the listener thread
            threading.Thread(target=self.__read_data).start()

            # Start the emitter if the port is valid
            _, port = self.soc.getsockname()
            if port > 0:
                self.emitter.start()
            return port
        except socket.error as msg:
            print("Failed to create socket. Error Code : " + str(msg[0]) + " Message " + msg[1])
            return

    def stop(self):
        print("Stopping")
        self.stopping = True
        self.soc.settimeout(0.0001)

    def __read_data(self):
        # Create an event loop for writing to Redis in the background
        futures = []
        loop = asyncio.new_event_loop()
        async_loop_thread = threading.Thread(target=loop.run_forever)
        async_loop_thread.start()

        # For sending batches
        queued_snapshots = []

        # For the reader to merge real-time and db data
        reader.init_thing_queue(self.thing)

        # To avoid sending out of order data
        prev_snapshot = {"ts": -1}

        print("Started listening for data from thing " + self.thing.thing_id)
        # Read forever until something causes a stoppage
        while True:
            try:
                # Wait for data from thing
                message, _ = self.soc.recvfrom(4096)

                # Handle manual stop
                if self.stopping:
                    raise Exception("Stopping")

                # Handle first connection
                if not self.connected:
                    self.connected = True
                    print("Thing " + self.thing.thing_id + " started streaming!")
                    self.publisher.publish_connection()
                    self.soc.settimeout(
                        DISCONNECT_TIMEOUT
                    )  # TODO: Change timeout depending on freq

                # Parse the data into a snapshot
                data_snapshot = self.parser.parse_telemetry_message(message)

                # Emit and store the snapshot if valid and in order
                if data_snapshot and prev_snapshot["ts"] < data_snapshot["ts"]:
                    prev_snapshot = data_snapshot

                    # Emit data via socket.io
                    self.emitter.push_data(data_snapshot)

                    # Store data in Redis in batches of 25
                    queued_snapshots.append(data_snapshot)
                    if len(queued_snapshots) == BATCH_SIZE:
                        futures.append(
                            asyncio.run_coroutine_threadsafe(
                                self.publisher.push_snapshots(queued_snapshots.copy()), loop
                            )
                        )
                        queued_snapshots.clear()

                    # Store in the long queue of the redis reader
                    reader.push_queue_snapshot(self.thing.thing_id, data_snapshot)

                # Clean up the futures as they complete
                for future in futures:
                    if future._state == "FINISHED":
                        futures.remove(future)
            except Exception as e:
                print(e)

                # Wait for all Redis writing to complete
                for future in futures:
                    future.result()
                loop.call_soon_threadsafe(loop.stop)
                async_loop_thread.join()

                # Clean up objects
                self.publisher.publish_disconnection()
                reader.destory_thing_queue(self.thing.thing_id)
                self.emitter.stop()

                # Destroy the session coordinator
                if self.close_callback:
                    self.close_callback(self.thing.thing_id)

                print("Thing " + self.thing.thing_id + " stopped streaming!")
                break
