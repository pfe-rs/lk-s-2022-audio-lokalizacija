#include <Wire.h>

#define MULTICAST_ADDR 0x10
#define SINGLECAST_ADDR 0x11

volatile bool recording = false;
long recStart, recEnd;

void timeSync() {
  Wire.read();
  if (!recording) {
    recStart = micros();
    recording = true;
  } else {
    recEnd = micros();
    recording = false;
    singleCastMode();
  }
}


void sendMeasurement() {
  Serial.println("Sending data...");
  // Wire.read();
  //// algoritam za slanjes
  Wire.write(1);

  ///

  multiCastMode();
}

void singleCastMode() {
  Wire.begin(SINGLECAST_ADDR);
  Wire.onRequest(sendMeasurement);
}

void multiCastMode() {
  Wire.begin(MULTICAST_ADDR);
  Wire.onReceive(timeSync);
}

void setup() {
  Serial.begin(115200);
  multiCastMode();
}

void loop() {
  Serial.println("waiting for command...");
  while (!recording) {}
  Serial.println("Recording...");
  while (recording) {}
  Serial.println("Done recording...");
}
