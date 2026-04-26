#include "gd_spi_utils.h"

#include <Arduino.h>
#include <SPI.h>

static uint8_t s_csb_pin = 10;
static uint32_t s_spi_clock_hz = 1000;

static uint32_t build_frame(uint8_t rw, uint8_t addr, uint16_t data) {
  uint32_t frame = 0;

  frame |= ((uint32_t)(rw & 0x01)) << 23;
  frame |= ((uint32_t)(addr & 0x1F)) << 18;
  frame |= ((uint32_t)(data & 0x03FF)) << 8;

  frame |= Calculate_SPI_CRC((uint16_t)(frame >> 8));
  return frame;
}

static uint32_t transfer_frame24(uint32_t frame) {
  uint32_t rx = 0;
  rx |= ((uint32_t)SPI.transfer((frame >> 16) & 0xFF)) << 16;
  rx |= ((uint32_t)SPI.transfer((frame >> 8) & 0xFF)) << 8;
  rx |= (uint32_t)SPI.transfer(frame & 0xFF);
  return rx;
}

void gd_spi_init(uint8_t csb_pin, uint32_t spi_clock_hz) {
  s_csb_pin = csb_pin;
  s_spi_clock_hz = spi_clock_hz;

  pinMode(s_csb_pin, OUTPUT);
  digitalWrite(s_csb_pin, HIGH);
  SPI.begin();
}

uint8_t Calculate_SPI_CRC(uint16_t wData) {
  uint8_t crc = 0x42;
  uint8_t data[2] = {(uint8_t)((wData >> 8) & 0xFF), (uint8_t)(wData & 0xFF)};

  for (uint8_t i = 0; i < 2; ++i) {
    crc ^= data[i];
    for (uint8_t bit = 0; bit < 8; ++bit) {
      uint8_t msb = (uint8_t)(crc & 0x80);
      crc <<= 1;
      if (msb) {
        crc ^= 0x2F;
      }
    }
  }

  return crc;
}

uint32_t gd_spi_read24(void) {
  uint32_t value = 0;

  digitalWrite(s_csb_pin, LOW);
  SPI.beginTransaction(SPISettings(s_spi_clock_hz, MSBFIRST, SPI_MODE0));

  value = transfer_frame24(0);

  SPI.endTransaction();
  digitalWrite(s_csb_pin, HIGH);

  return value;
}

uint32_t send_GD_DC(uint8_t dx, uint8_t rw, uint8_t addr, uint16_t data) {
  uint32_t rx = 0;
  uint32_t nop_frame = build_frame(0, 0, 0);
  uint32_t req_frame = build_frame(rw, addr, data);

  digitalWrite(s_csb_pin, LOW);
  SPI.beginTransaction(SPISettings(s_spi_clock_hz, MSBFIRST, SPI_MODE0));

  for (uint8_t i = 0; i < dx; ++i) {
    (void)transfer_frame24(nop_frame);
  }

  (void)transfer_frame24(req_frame);
  rx = transfer_frame24(nop_frame);

  SPI.endTransaction();
  digitalWrite(s_csb_pin, HIGH);

  return rx;
}
