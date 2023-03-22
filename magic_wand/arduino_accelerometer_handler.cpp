
/* Copyright 2019 The TensorFlow Authors. All Rights Reserved.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
==============================================================================*/

#if defined(ARDUINO) && !defined(ARDUINO_ARDUINO_NANO33BLE)
#define ARDUINO_EXCLUDE_CODE
#endif  // defined(ARDUINO) && !defined(ARDUINO_ARDUINO_NANO33BLE)

#ifndef ARDUINO_EXCLUDE_CODE

#include "accelerometer_handler.h"

#include <Arduino.h>
#include <Arduino_LSM9DS1.h>

#include "constants.h"

// A buffer holding the last 200 sets of 3-channel values
float save_data[300] = {0.0};
// Most recent position in the save_data buffer
int begin_index = 0;
// True if there is not yet enough data to run inference
bool pending_initial_data = true;
// How often we should save a measurement during downsampling
int sample_every_n;
// The number of measurements since we last saved one
int sample_skip_counter = 1;

TfLiteStatus SetupAccelerometer(tflite::ErrorReporter* error_reporter) {
  // Switch on the IMU
  if (!IMU.begin()) {
    TF_LITE_REPORT_ERROR(error_reporter, "Failed to initialize IMU");
    return kTfLiteError;
  }

  // Make sure we are pulling measurements into a FIFO.
  // If you see an error on this line, make sure you have at least v1.1.0 of the
  // Arduino_LSM9DS1 library installed.
  IMU.setContinuousMode();
    TF_LITE_REPORT_ERROR(error_reporter,
                         "set MOde\n");
  // Determine how many measurements to keep in order to
  // meet kTargetHz
  float sample_rate = IMU.accelerationSampleRate();
  sample_every_n = static_cast<int>(roundf(sample_rate / kTargetHz));

  TF_LITE_REPORT_ERROR(error_reporter, "Magic starts!");

  return kTfLiteOk;
}

bool ReadAccelerometer(tflite::ErrorReporter* error_reporter, float* input,
                       int length) {
  // Keep track of whether we stored any new data
  bool new_data = false;
  // Loop through new samples and add to buffer
  while (IMU.accelerationAvailable()) {
    float x, y, z;
    // Read each sample, removing it from the device's FIFO buffer
    if (!IMU.readAcceleration(x, y, z)) {
      TF_LITE_REPORT_ERROR(error_reporter, "Failed to read data");
      break;
    }
    // Throw away this sample unless it's the nth
    if (sample_skip_counter != sample_every_n) {
      sample_skip_counter += 1;
      continue;
    }
    const float norm_x = x;
    const float norm_y = y;
    const float norm_z = z;
//        TF_LITE_REPORT_ERROR(error_reporter, "data-x:%f,y:%f,z:%f\n",
//                         x,y,z);
    save_data[begin_index++] = norm_x * 1000;
    save_data[begin_index++] = norm_y * 1000;
    save_data[begin_index++] = norm_z * 1000;
    // Since we took a sample, reset the skip counter
    sample_skip_counter = 1;
    // If we reached the end of the circle buffer, reset
    if (begin_index >= 300) {
      begin_index = 0;
    }
    new_data = true;
//    if(!IMU.accelerationAvailable())
//       TF_LITE_REPORT_ERROR(error_reporter, "NOOOOOOOOOOOOOOOOOOOOOOOOOOO\n");
  }

  // Skip this round if data is not ready yet
  if (!new_data) {
    return false;
  }

  // Check if we are ready for prediction or still pending more initial data
  if (pending_initial_data && begin_index >= 100) {
    pending_initial_data = false;
  }

  // Return if we don't have enough data
  if (pending_initial_data) {
    return false;
  }

//  TF_LITE_REPORT_ERROR(error_reporter, "begin-index:%d",
//                         begin_index);
  // Copy the requested number of bytes to the provided input tensor
  for (int i = 0; i < length; ++i) {
    
    int ring_array_index = begin_index + i - length;
    if (ring_array_index < 0) {
      ring_array_index += 300;
    }
    input[i] = save_data[ring_array_index];
  }
//  for(int i=0;i<length/3;i++){
//     TF_LITE_REPORT_ERROR(error_reporter, "%f,%f,%f,\n",input[3*i]/1000,input[3*i+1]/1000,input[3*i+2]/1000);
//  }

  return true;
}

#endif  // ARDUINO_EXCLUDE_CODE
