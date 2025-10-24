#ifndef ESERIAL_H
#define ESERIAL_H

#include "serial_types.h"

/**
 * inits serial message object from raw message bytes
 * returns 0 on success
 */
uint8_t init_SerialMessage_from_bytes(uint8_t *bytes , SerialMessage *msg);
/**
 * Determines the message type from cmd byte
 * returns Type enum
 */
SerialMessageType get_SerialMessageType_from_cmd(uint8_t cmd);
/**
 * makes raw bytes from serial message.
 * returns 0 on success
 */
uint8_t get_bytes_from_SerialMessage(uint8_t *bytes , SerialMessage *msg);
/**
 * Makes and inits a Write Serial Message.
 * Takes parameters and SerialMessage pointer memory
 * returns 0 on success
 */
uint8_t make_WriteSerialMessage(uint8_t addr , uint16_t data , uint8_t mid , SerialMessage *msg);
/**
 * Makes and inits a read Serial Message.
 * Takes parameters and SerialMessage pointer memory
 * returns 0 on success
 */
uint8_t make_ReadSerialMessage(uint8_t addr , uint8_t mid , SerialMessage *msg);
/**
 * Makes and inits an ACK Serial Message.
 * Takes parameters and SerialMessage pointer memory
 * returns 0 on success
 */
uint8_t make_ACKSerialMessage(uint8_t addr , uint16_t data , uint8_t mid , SerialMessage *msg);
#endif
