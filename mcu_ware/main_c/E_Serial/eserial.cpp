#include "eserial.h"

uint8_t init_SerialMessage_from_bytes(uint8_t *bytes , SerialMessage *msg){
    if(bytes == NULL)return 1;
    if(msg == NULL)return 2;

    msg->cmd = bytes[1];

    msg->addr = bytes[2];

    msg->data = bytes[3];
    msg->data <<= 8;
    msg->data |= bytes[4];

    msg->mid = bytes[5];

    msg->type = msg->cmd ;//get_SerialMessageType_from_cmd(msg->cmd);

    return 0;
}

SerialMessageType get_SerialMessageType_from_cmd(uint8_t cmd){
    switch (cmd)
    {
        case 0:
            return NOP;
            break;
        case 1:
            return ACK;
            break;
        case 2:
            return WR;
            break;
        case 3:
            return RE;
            break;
        default:
            return NOP;
            break;
    }
}

uint8_t get_bytes_from_SerialMessage(uint8_t *bytes , SerialMessage *msg){
    if(bytes == NULL)return 1;
    if(msg == NULL)return 2;
    bytes[0] = SERIAL_DELI;
    bytes[1] = msg->cmd;
    bytes[2] = msg->addr;
    bytes[3] = (msg->data >> 8);
    bytes[4] = (msg->data & 0xFF);
    bytes[5] = msg->mid;
    return 0;
}

uint8_t make_ACKSerialMessage(uint8_t addr , uint16_t data , uint8_t mid , SerialMessage *msg){
    if(msg == NULL)return 1;
    msg->cmd = ACK;
    
    msg->addr = addr;

    msg->data = data;

    msg->mid = mid;
    
    return 0;
}

uint8_t make_WriteSerialMessage(uint8_t addr , uint16_t data , uint8_t mid , SerialMessage *msg){
    if(msg == NULL)return 1;
    msg->cmd = WR;
    
    msg->addr = addr;

    msg->data = data;

    msg->mid = mid;

    return 0;
}

uint8_t make_ReadSerialMessage(uint8_t addr , uint8_t mid , SerialMessage *msg){
    if(msg == NULL)return 1;
    msg->cmd = RE;
    
    msg->addr = addr;

    msg->data = 0;

    msg->mid = mid;

    return 0;
}