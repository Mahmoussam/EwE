#ifndef SERIAL_TYPES_H
#define SERIAL_TYPES_H

#include <stdint.h>

#define SERIAL_DELI  '!'
#define CMD_LEN   1
#define ADDR_LEN  1
#define DATA_LEN  2
#define DX_LEN    1
#define MID_LEN   1
#define MSG_LEN  (1 + CMD_LEN + ADDR_LEN + DATA_LEN + DX_LEN + MID_LEN)

typedef enum{
    NOP = 0,
    ACK = 1,
    WR = 2,
    RE = 3,
}SerialMessageType;

/**
 * Serial message structure
 * Has:
 *  cmd
 *  addr
 *  data or value
 *  ID ,just a counter based so far ,counted at host side..
 * 
 *     # raw binary (example format: "!CADDXI")  C for cmd, D for data, X for dx, I for ID
 */
typedef struct{
    uint16_t data;
    
    uint8_t cmd;
    uint8_t addr;
    uint8_t dx;
    uint8_t mid;
    
    SerialMessageType type;
}SerialMessage;

#endif
