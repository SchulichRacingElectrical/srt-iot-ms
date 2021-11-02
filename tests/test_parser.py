# Copyright Schulich Racing FSAE
# Written By Justin Tijunelis

import pytest
from iot.parser import Parser

@pytest.fixture(scope='module')
def parser():
  parser = Parser([])
  yield parser
  del parser

@pytest.mark.parametrize('sensor_ids, result', [
  ("", ""),
  # Integer tests
  ("d", "<i"),
  ("dd", "<ii"),
  ("ddd", "<iii")
  # Double tests
  # Short tests
  # Char tests
  # Mixed tests
])
def test_parser_data_format(parser, sensor_ids, result):
  assert parser.get_data_format(sensor_ids) == result
