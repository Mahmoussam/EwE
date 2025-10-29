
#include "eserial.h"


#define MSG_SIZE 6
#define START_BYTE '!'

byte rxBuffer[MSG_SIZE];
byte rxIndex = 0;
bool msgReady = false;

bool state13 = false;
void setup() {
  Serial.begin(9600);
  while (!Serial) {
    delay(10);
  }
  
  pinMode(13 , OUTPUT);
}

// ------------------------------------------------------
// Function: sendMessage
// Sends a full 6-byte message
// ------------------------------------------------------
void sendMessage(const byte *msg) {
  Serial.write(msg, MSG_SIZE);
}

// ------------------------------------------------------
// Function: onMessageReceived
// Called when a full valid message is received
// ------------------------------------------------------
void onMessageReceived(const byte *raw_msg) {
  
  // Example: echo back the same message
  SerialMessage msg;
  if(init_SerialMessage_from_bytes(raw_msg , &msg) == 0){
    state13 = !state13;
    digitalWrite(13 , state13);
    SerialMessage response;
    make_ACKSerialMessage(msg.addr , msg.data , msg.mid , &response);
    char out[6];
    get_bytes_from_SerialMessage(out , &response);
    sendMessage(out);
  }

  
}

// ------------------------------------------------------
// Function: serialEvent
// Called automatically by Arduino core between loop() calls
// ------------------------------------------------------
void serialEvent() {
  while (Serial.available() > 0) {
    byte b = Serial.read();

    // If we’re at start and see START_BYTE, begin buffering
    if (rxIndex == 0 && b != START_BYTE)
      continue;  // ignore until we see '!'
    
    rxBuffer[rxIndex++] = b;

    if (rxIndex >= MSG_SIZE) {
      rxIndex = 0;
      msgReady = true;
      onMessageReceived(rxBuffer);
    }
  }
}

// ------------------------------------------------------
// Main loop
// ------------------------------------------------------
void loop() {
  // Example: periodically send a message
  static unsigned long lastSend = 0;
  if (millis() - lastSend > 3000) {
    lastSend = millis();

    byte msg[MSG_SIZE] = {START_BYTE, 'H', 'E', 'L', 'L', 'O'};
    sendMessage(msg);
  }
  serialEvent();
  // (serialEvent() runs automatically between loop iterations)
}
