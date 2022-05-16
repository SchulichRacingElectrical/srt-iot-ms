# Copyright Schulich Racing FSAE
# Written By Justin Tijunelis, Camilla Abdrazakov, Jonathan Mulyk

import sys
import socket
import threading
import asyncio
import time
from ..utils.parser import Parser
from ..redis.publisher import publisher

CONNECTION_TIMEOUT = 10.0
MESSAGE_TIMEOUT = 3.0

"""
UDP variable frequency data receiver from telemetry hardware. 
"""
class SessionReceiver:
  def __init__(self, sensors, coordinator):
    self.coordinator = coordinator
    self.parser = Parser(sensors)
    self.connected = False
    self.stopping = False

  def start(self):
    self.soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
      self.soc.bind(('', 0))
      self.soc.settimeout(CONNECTION_TIMEOUT)
    except socket.error as msg:
      self.coordinator.notify("error")
      return -1
    def loop():
      asyncio.run(self.__read_data())
    self.udp_listener = threading.Thread(target=loop)
    self.udp_listener.start()
    _, port = self.soc.getsockname()
    return port

  def stop(self):
    self.stopping = True
    self.soc.settimeout(0.0001)

  def __read_data(self):
    # Create an event loop for writing to Redis in the background
    futures = []
    queuedSnapshots = []
    prev_snapshot = {"ts": -1}
    loop = asyncio.new_event_loop()
    threading.Thread(target=loop.run_forever).start()

    # Read forever until something causes a stoppage
    while True:
      try:
        # Wait for data from thing
        message, _ = self.soc.recvfrom(4096)

        # Handle first connection
        if not self.connected:
          self.coordinator.notify("connection")
          self.connected = True
          self.soc.settimeout(MESSAGE_TIMEOUT)
        
        # Handle manual stop
        if self.stopping: raise Exception("Stopping")
        
        # Parse the data into a snapshot
        data_snapshot = self.parser.parse_telemetry_message(message)

        # Emit and store the snapshot if valid and in order
        if data_snapshot and prev_snapshot["ts"] < data_snapshot["ts"]:
          prev_snapshot = data_snapshot

          # Emit data via socket.io - TODO: Should this be called in the background?
          self.coordinator.emit_snapshot(data_snapshot)

          # Store data in Redis
          futures.append(
            asyncio.run_coroutine_threadsafe(
              self.coordinator.write_snapshot(data_snapshot),
              loop
            )
          )

        # Clean up the futures as they complete
        for future in futures:
          if future._state == "FINISHED":
            futures.remove(future)
      except:
        for future in futures:
         future.result()
        loop.call_soon_threadsafe(loop.stop)
        if not self.stopping:
          self.coordinator.notify("disconnection")
        return
