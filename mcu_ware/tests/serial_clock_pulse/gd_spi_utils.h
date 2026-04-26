#ifndef GD_SPI_UTILS_H
#define GD_SPI_UTILS_H

#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

void gd_spi_init(uint8_t csb_pin, uint32_t spi_clock_hz);
uint8_t Calculate_SPI_CRC(uint16_t wData);
uint32_t gd_spi_read24(void);
uint32_t send_GD_DC(uint8_t dx, uint8_t rw, uint8_t addr, uint16_t data);

#ifdef __cplusplus
}
#endif

#endif
