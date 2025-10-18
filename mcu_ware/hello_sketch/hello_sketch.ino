void setup() {
  Serial.begin(9600);

  while (!Serial) {
    delay(100); // wait for serial port to connect
  }
}

void loop() {
  //echo
  while (Serial.available() > 0) {
    byte b = Serial.read();
    Serial.write(b);  // write the same byte back, unchanged
  }
  // Send your message
  Serial.print("!ABCD");
  
  // Wait for 1 second
  delay(1000);
}
