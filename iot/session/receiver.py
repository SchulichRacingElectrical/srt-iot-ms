# Copyright Schulich Racing FSAE
# Written By Justin Tijunelis, Camilla Abdrazakov, Jonathan Mulyk

import sys
import socket
import threading
import asyncio
import time
from ..utils.parser import Parser

CONNECTION_TIMEOUT = 10.0
MESSAGE_TIMEOUT = 3.0

"""
UDP variable frequency data receiver from telemetry hardware. 
"""
class SessionReceiver:
  def __init__(self, sensors, coordinator):
    self.coordinator = coordinator
    self.connected = False
    self.stopping = False
    self.parser = Parser(sensors)

  def start(self):
    self.soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
      self.soc.bind(('', 0))
      self.soc.settimeout(CONNECTION_TIMEOUT)
    except socket.error as msg:
      self.coordinator.notify("error") # TODO: Must call async
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

  async def __read_data(self):
    futures = []
    loop = asyncio.new_event_loop()
    threading.Thread(target=loop.run_forever).start()
    while True:
      try:
        message, _ = self.soc.recvfrom(4096)
        if self.stopping: raise Exception("Stopping")
        if not self.connected:
          await self.coordinator.notify("connection")
          self.connected = True
          self.soc.settimeout(MESSAGE_TIMEOUT)
        if len(message) < 6: continue
        data_snapshot = self.parser.parse_telemetry_message(message)
        if data_snapshot == {}: continue
        futures.append(
          asyncio.run_coroutine_threadsafe(
            self.coordinator.notify("snapshot", data_snapshot), 
            loop
          )
        )
        for future in futures:
          if future._state == "FINISHED":
            futures.remove(future)
      except:
        if not self.stopping:
          await self.coordinator.notify("disconnection")
        for future in futures:
          future.result()
          loop.call_soon_threadsafe(loop.stop)
        return
