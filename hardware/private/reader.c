// Copyright Schulich Racing FSAE
// Written by Justin Tijunelis

#include "../public/reader.h"

// Get the sensor data (should it be passed in?)
// Based the sensor list and the timestamp, 
// take modulus to determine which sensor to read

// Check if the value has changed, if not, do not include in data
// Return the sample in the correct format
struct Sample *read_CAN_data(int timestamp) {
  #if 0
  struct Sample sample;
  sample.length = "";
  sample.sensor_data = "0b";
  sample.sensor_ids = "";


  return &sample;
  #endif 

  return 0;
}