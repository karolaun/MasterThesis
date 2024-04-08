#include <Servo.h>
 
Servo myservo;  // create servo object
int pos = 0;    // storing servo position
 
void setup() {
  myservo.attach(9);  // standard to use pin 9 for servo
}
 
void loop() {
  for (pos = 0; pos <= 35; pos += 1) { // 0 to 35 degrees with steps of 1 degree
    myservo.write(pos);              // go to pos
    delay(15);                       // waits to reach pos
    Serial.print(pos);              // write to serial monitor to see results
  }
  for (pos = 35; pos >= 0; pos -= 1) {
    myservo.write(pos);            
    delay(15);                     
    Serial.print(pos);
  }
}