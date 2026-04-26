#include <SPI.h>

static uint8_t Calculate_SPI_CRC(uint16_t wData) {
  uint8_t crc = 0x42;
  uint8_t data[2] = {(uint8_t)((wData >> 8) & 0xFF), (uint8_t)(wData & 0xFF)};

  for (uint8_t i = 0; i < 2; ++i) {
    crc ^= data[i];
    for (uint8_t bit = 0; bit < 8; ++bit) {
      uint8_t msb = (uint8_t)(crc & 0x80);
      crc <<= 1;
      if (msb) crc ^= 0x2F;
    }
  }

  return crc;
}

const uint8_t CSB_PIN = 10;

uint32_t read24BitsSPI() {
  uint32_t value = 0;
  digitalWrite(CSB_PIN, LOW);
  SPI.beginTransaction(SPISettings(1000, MSBFIRST, SPI_MODE0)); // 1 kHz SPI clock

  value |= ((uint32_t)SPI.transfer(0x00)) << 16;
  value |= ((uint32_t)SPI.transfer(0x00)) << 8;
  value |= ((uint32_t)SPI.transfer(0x00));
  digitalWrite(CSB_PIN, HIGH);
    
  SPI.endTransaction();

  return value;
}

uint32_t gd3160_spi_transfer(uint8_t rw,
                             uint8_t addr,
                             uint16_t data)
{
    uint32_t frame = 0;

    frame |= ((uint32_t)(rw & 0x01)) << 23;
    frame |= ((uint32_t)(addr & 0x1F)) << 18;
    frame |= ((uint32_t)(data & 0x03FF)) << 8;

    uint8_t crc = Calculate_SPI_CRC(frame>>8);
    frame |= crc;

    uint32_t rx = 0;

    digitalWrite(CSB_PIN, LOW);

    SPI.beginTransaction(SPISettings(1000, MSBFIRST, SPI_MODE0)); // 1 kHz SPI clock
    rx |= ((uint32_t)SPI.transfer((frame >> 16) & 0xFF)) << 16;
    rx |= ((uint32_t)SPI.transfer((frame >> 8)  & 0xFF)) << 8;
    rx |= ((uint32_t)SPI.transfer(frame & 0xFF));
    SPI.endTransaction();

    digitalWrite(CSB_PIN, HIGH);

    return rx;
}

uint32_t DC_send(uint8_t rw,
                             uint8_t addr,
                             uint16_t data)
{
    uint32_t frame = 0;

    frame |= ((uint32_t)(rw & 0x01)) << 23;
    frame |= ((uint32_t)(addr & 0x1F)) << 18;
    frame |= ((uint32_t)(data & 0x03FF)) << 8;

    uint8_t crc = Calculate_SPI_CRC(frame>>8);
    frame |= crc;

    uint32_t rx = 0;

    digitalWrite(CSB_PIN, LOW);

    SPI.beginTransaction(SPISettings(1000, MSBFIRST, SPI_MODE0)); // 1 kHz SPI clock

    rx |= ((uint32_t)SPI.transfer((frame >> 16) & 0xFF)) << 16;
    rx |= ((uint32_t)SPI.transfer((frame >> 8)  & 0xFF)) << 8;
    rx |= ((uint32_t)SPI.transfer(frame & 0xFF));
    Serial.print("RX1: 0x");
    Serial.println(rx, HEX);

    rx = 0;
    rx |= ((uint32_t)SPI.transfer((0) & 0xFF)) << 16;
    rx |= ((uint32_t)SPI.transfer((0)  & 0xFF)) << 8;
    rx |= ((uint32_t)SPI.transfer(Calculate_SPI_CRC(0) & 0xFF));
    
    Serial.print("RX2: 0x");
    Serial.println(rx, HEX);

    SPI.endTransaction();

    digitalWrite(CSB_PIN, HIGH);

    return rx;
}
void printHexValue(uint32_t value){
    if (value < 0x100000) Serial.print('0');
    if (value < 0x10000)  Serial.print('0');
    if (value < 0x1000)   Serial.print('0');
    if (value < 0x100)    Serial.print('0');
    if (value < 0x10)     Serial.print('0');
    Serial.println(value, HEX);

}
void setup() {
  pinMode(CSB_PIN, OUTPUT);
  digitalWrite(CSB_PIN, HIGH);

  SPI.begin();
  Serial.begin(9600);
  while (!Serial) {}

  Serial.println("Type any character to read 24 SPI bits.");
}

void loop() {
  if (Serial.available() > 0) {
    int addrInput = Serial.parseInt();

    //uint32_t value = read24BitsSPI();
    //Serial.print("Next 24-bit SPI value: 0x");
    //printHexValue(value);

    
    while (Serial.available() > 0) Serial.read();

    if (addrInput < 0 || addrInput > 31) {
      Serial.println("Invalid addr. Enter 0-31.");
      return;
    }

    uint8_t addr = (uint8_t)addrInput;
    uint32_t rx = DC_send(0, addr, 0);
    delay(10);
  
    uint32_t value = read24BitsSPI();

    Serial.print("Next 24-bit SPI value: 0x");
    printHexValue(value);
    
  } 
}