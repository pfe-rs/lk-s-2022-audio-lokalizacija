#include <Wire.h>

#define MULTICAST_ADDR 0x10
#define SINGLECAST_ADDR 0x11

void setup() {
  Serial.begin(115200);
  Wire.begin();
  delay(1000);
  
  Serial.println("Multicast send");
  Wire.beginTransmission(MULTICAST_ADDR);
  Wire.write(0);
  Wire.endTransmission(MULTICAST_ADDR);
  delay(2000);
  
  Serial.println("Multicast send");
  Wire.beginTransmission(MULTICAST_ADDR);
  Wire.write(0);
  Wire.endTransmission(MULTICAST_ADDR);
  delay(2000);

  Serial.println("Request data");
  Wire.requestFrom(SINGLECAST_ADDR, 1);
  Serial.println("Get data");
}

void loop() {
  // put your main code here, to run repeatedly:

}
