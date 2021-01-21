#include "Compiler_Errors.h"
#include <MPR121.h>
#include <MPR121_Datastream.h>
#include <Wire.h>

const uint32_t BAUD_RATE = 115200;
const uint8_t MPR121_ADDR = 0x5C;
const uint8_t MPR121_INT = 4;

const bool MPR121_DATASTREAM_ENABLE = false;

const uint8_t FILL_THRESHOLD = 10; //Amount of empty samples before filling the rest (of the time windoes) with zeros.

#define numElectrodes 12
#define DELIMITER ","

void setup() {
  Serial.begin(BAUD_RATE);
  pinMode(LED_BUILTIN, OUTPUT);

  if (!MPR121.begin(MPR121_ADDR)) {
    Serial.println("error setting up MPR121");
    switch (MPR121.getError()) {
      case NO_ERROR:
        Serial.println("no error");
        break;
      case ADDRESS_UNKNOWN:
        Serial.println("incorrect address");
        break;
      case READBACK_FAIL:
        Serial.println("readback failure");
        break;
      case OVERCURRENT_FLAG:
        Serial.println("overcurrent on REXT pin");
        break;
      case OUT_OF_RANGE:
        Serial.println("electrode out of range");
        break;
      case NOT_INITED:
        Serial.println("not initialised");
        break;
      default:
        Serial.println("unknown error");
        break;
    }
    while (1);
  }

  MPR121.setInterruptPin(MPR121_INT);

  if (MPR121_DATASTREAM_ENABLE) {
    MPR121.restoreSavedThresholds();
    MPR121_Datastream.begin(&Serial);
  } else {
    MPR121.setTouchThreshold(20);
    MPR121.setReleaseThreshold(20);
  }

  MPR121.setFFI(FFI_10);
  MPR121.setSFI(SFI_10);
  MPR121.setGlobalCDT(CDT_4US);
  
  digitalWrite(LED_BUILTIN, HIGH);
  delay(1000);
  MPR121.autoSetElectrodes();
  digitalWrite(LED_BUILTIN, LOW);
}

void loop() {
  
  MPR121.updateAll();

  for (int i=0; i < 12; i++) { // Looping through the areas.
    
    if (MPR121.isNewTouch(i)) { // Checking if an area is touched.
      digitalWrite(LED_BUILTIN, HIGH);
      int empty_samples = 0; // Number of empty samples in a row.
      for(int j=0; j<100; j++){ // Looping through 100*0.035 seconds.
        
        if (empty_samples == FILL_THRESHOLD){ // If X empty samples, fill the rest with zeros and break.
          for(int l=j; l<100; l++){
            for(int k=0; k<12; k++){
              Serial.print(0);
              if ((k+1) < numElectrodes){ // Printing delimiter between each value.
                Serial.print(DELIMITER);
              }
            }
            Serial.println();
          }
          break;
        }

        int LOW_electrodes = 0; // Number of LOW electrodes in a sample.
         
        for(int k=0; k<12; k++){
          MPR121.updateFilteredData();
          //Serial.print(MPR121.getTouchData(k));
          //Serial.print(MPR121.getFilteredData(k));
          int delta = MPR121.getBaselineData(k) - MPR121.getFilteredData(k);
          if (delta > 5){
            Serial.print(delta);         
          } else {
            Serial.print(0);
            LOW_electrodes++;
            if (LOW_electrodes == 12){
              empty_samples++;
            }
          }
          if ((k+1) < numElectrodes){ // Printing delimiter between each value.
            Serial.print(DELIMITER);
          }
        }
        Serial.println();
        delay(0); //Set the delay to tweak the sample frequency.
      } 
    } 
  }

  if (MPR121_DATASTREAM_ENABLE) {
    MPR121_Datastream.update();
  }
}
