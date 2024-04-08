//This code is taken directly from the github page linked below.
//https://github.com/ralbra/Optical_Flow_Sensors_Arduino/blob/master/examples/PMW3901_Framebuffer_LCD/PMW3901_Framebuffer_LCD.ino
 
#include "Optical_Flow_Sensor.h"
 
// param #1 digital pin 4 for chip select
// param #2 sensor type either PAA5100 or PMW3901
Optical_Flow_Sensor flow(4, PAA5100);
 
void setup() {
  Serial.begin(9600);
 
  if (!flow.begin()) {
    Serial.println("Initialization of the flow sensor failed");
    while(1) { }
  }
 
}
 
int16_t deltaX,deltaY;
 
void loop() {
  // Get motion count since last call
  flow.readMotionCount(&deltaX, &deltaY);
 
  Serial.print("X: ");
  Serial.print(deltaX);
  Serial.print(", Y: ");
  Serial.print(deltaY);
  Serial.print("\n");
 
  delay(100);
}