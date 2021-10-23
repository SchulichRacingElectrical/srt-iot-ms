// Copyright Schulich Racing FSAE
// Written by Justin Tijunelis
#ifndef READER
#define READER

#pragma once

struct Sample {
  unsigned char length;
  unsigned char *sensor_ids;
  unsigned char *sensor_data;
};

/*
*
*/
struct Sample *read_CAN_data(int timestamp);

#endif