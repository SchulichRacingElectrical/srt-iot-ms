# Copyright Schulich Racing FSAE
# Written By Justin Tijunelis

import pytest
from iot.parser import Parser
from iot.sensors import Sensors

@pytest.fixture(scope='module')
def parser():
  sensors = Sensors('', '')
  sensors.set_sensor_list([{
    "name": "Longitude",
    "sensor_id": 1,
    "type": "d"
  }, {
    "name": "X",
    "sensor_id": 2,
    "type": "f"
  }, {
    "name": "Rotary Pot",
    "sensor_id": 3,
    "type": "e"
  }, {
    "name": "RPM",
    "sensor_id": 4,
    "type": "h"
  }, {
    "name": "Display ON",
    "sensor_id": 5,
    "type": "?"
  }, {
    "name": "RPM Lights",
    "sensor_id": 6,
    "type": "c"
  }, {
    "name": "UTC",
    "sensor_id": 7,
    "type": "q"
  }, {
    "name": "Gear",
    "sensor_id": 8,
    "type": "i"
  }])
  parser = Parser(sensors)
  yield parser
  del parser

def test_parser_data_format_empty(parser):
  assert parser.get_data_format("") == ""

@pytest.mark.parametrize('sensor_ids, result', [
  # Integer tests
  ([8], "<i"),
  ([8, 8], "<ii"),
  ([8, 8, 8], "<iii"),
  # Double tests
  ([1], "<d"),
  ([1, 1], "<dd"),
  ([1, 1, 1], "<ddd"),
  # Short/Short Float tests
  ([4], "<hxx"),
  ([4, 4], "<hh"),
  ([4, 4, 4], "<hhhxx"),
  # Char/Bool tests
  ([6], "<cxxx"),
  ([6, 6], "<ccxx"),
  ([6, 6, 6], "<cccx"),
  ([6, 6, 6, 6], "<cccc"),
  ([6, 6, 6, 6, 6], "<cccccxxx"),
])
def test_parser_single_data_type_format(parser, sensor_ids, result):
  assert parser.get_data_format(sensor_ids) == result

@pytest.mark.parametrize('sensor_ids, result', [
  ([7, 1, 2, 8, 4, 6, 5, 3], "<qdfihc?exx"),
  ([7, 4, 8, 5, 2, 6, 1], "<qhxxi?xxxfcxxxd"),
  ([4, 3, 6, 5, 6, 5, 2, 8, 3, 8], "<hec?c?fiexxi")
])
def test_parser_multi_data_type_format(parser, sensor_ids, result):
  assert parser.get_data_format(sensor_ids) == result

