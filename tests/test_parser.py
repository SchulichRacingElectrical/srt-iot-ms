# Copyright Schulich Racing FSAE
# Written By Justin Tijunelis

import pytest
from iot.parser import Parser

# TODO: Create sensor list

@pytest.fixture(scope='module')
def parser():
  parser = Parser([])
  yield parser
  del parser

def test_parser_data_format_empty(parser):
  assert parser.get_data_format("") == ""

@pytest.mark.parametrize('sensor_ids, result', [
  # Integer tests
  ("d", "<i"),
  ("dd", "<ii"),
  ("ddd", "<iii"),
  # Double tests
  ("b", "<d"),
  ("bb", "<dd"),
  ("bbb", "<ddd"),
  # Short/Short Float tests
  ("e", "<hxx"),
  ("ee", "<hh"),
  ("eee", "<hhhxx"),
  # Char/Bool tests
  ("f", "<cxxx"),
  ("ff", "<ccxx"),
  ("fff", "<cccx"),
  ("ffff", "<cccc"),
  ("fffff", "<cccccxxx"),
])
def test_parser_single_data_type_format(parser, sensor_ids, result):
  assert parser.get_data_format(sensor_ids) == result

@pytest.mark.parametrize('sensor_ids, result', [
  ("abcdefgh", "<qdfihc?exx"),
  ("aedgcfb", "<qhxxi?xxxfcxxxd"),
  ("ehfgfgcdhd", "<hec?c?fiexxi")
])
def test_parser_multi_data_type_format(parser, sensor_ids, result):
  assert parser.get_data_format(sensor_ids) == result