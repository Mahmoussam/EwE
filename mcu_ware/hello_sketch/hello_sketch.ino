void setup() {
  Serial.begin(9600);

  while (!Serial) {
    delay(100); // wait for serial port to connect
  }

  Serial.print("!AKHi#");
}

void loop() {
  // Send your message
  Serial.print("!AKREP");

  // Wait for 1 second
  delay(1000);
}
