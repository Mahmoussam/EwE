
#include <SPI.h>

#include "eserial.h"

// Chip select pin
#define SS 10


#define MSG_SIZE 6
#define START_BYTE '!'

byte rxBuffer[MSG_SIZE];
byte rxIndex = 0;
bool msgReady = false;

bool state13 = false;
void setup() {
  // Serial comm to PC init
  Serial.begin(9600);
  while (!Serial) {
    delay(10);
  }
  // SPI to GD init
  
  pinMode(SS, OUTPUT);
  digitalWrite(SS, HIGH);

  SPI.begin();
  SPI.beginTransaction(SPISettings(
    4000000,     // 4 MHz
    MSBFIRST,
    SPI_MODE0
  ));
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


uint32_t gd3160_spi_transfer(uint8_t rw,
                             uint8_t addr,
                             uint16_t data)
{
    uint32_t frame = 0;

    frame |= ((uint32_t)(rw & 0x01)) << 23;
    frame |= ((uint32_t)(addr & 0x1F)) << 18;
    frame |= ((uint32_t)(data & 0x03FF)) << 8;

    uint8_t crc = gd3160_crc8(frame);//not yet included ..but implemented indeed..
    frame |= crc;

    uint32_t rx = 0;

    digitalWrite(SS, LOW);

    rx |= ((uint32_t)SPI.transfer((frame >> 16) & 0xFF)) << 16;
    rx |= ((uint32_t)SPI.transfer((frame >> 8)  & 0xFF)) << 8;
    rx |= ((uint32_t)SPI.transfer(frame & 0xFF));

    digitalWrite(SS, HIGH);

    return rx;
}

