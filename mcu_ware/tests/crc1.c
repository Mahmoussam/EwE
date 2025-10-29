#include <stdio.h>
#include <assert.h>
#include "../GD3160/GD3160.h"
/**
 * CRC function that utilizes same concept of the lookup table..
 */
uint8_t CALC_CRC8_table(uint16_t wData);
/**
 * CRC function with same specs for shift approach as per datasheet
 */
uint8_t CALC_CRC8_shift(uint16_t wData);

int32_t main(){

    printf("Test val for 0x3100 : 0X%0X \n" ,Calculate_SPI_CRC(0x3100));
    printf("Test val for 0x1234 : 0X%0X \n" ,Calculate_SPI_CRC(0x1234));
    for(uint32_t test_data = 0;test_data < (((uint32_t)1)<<16);test_data++){
        //assert(Calculate_SPI_CRC(test_data) == CALC_CRC8_table(test_data));
        if(Calculate_SPI_CRC(test_data) != CALC_CRC8_table(test_data)){
            printf("Invalid#1 @ 0X%0X \n" , test_data);
            return 0;
        }
        //printf("0x%0X\n",Calculate_SPI_CRC(test_data));
    }

    puts("CRC Table vs CRC shifting using same polynomial and seed : Valid ..");


     for(uint32_t test_data = 0;test_data < (((uint32_t)1)<<16);test_data++){
        //assert(Calculate_SPI_CRC(test_data) == CALC_CRC8_table(test_data));
        if(Calculate_SPI_CRC(test_data) != CALC_CRC8_shift(test_data)){
            printf("Invalid#2 @ 0X%0X \n" , test_data);
            return 0;
        }
        //printf("0x%0X\n",Calculate_SPI_CRC(test_data));
    }

    puts("CRC Table vs CRC shifting using data sheet specs.. : Valid ..");

    return 0;
}


uint8_t CALC_CRC8_table(uint16_t wData){
    uint8_t data[2] = {wData >> 8 , wData & 0xFF};
    uint8_t crc = 0x42;
    for(int i = 0;i < 2;i++){
        crc ^= data[i];
        for(uint8_t d = 0;d < 8;d++){
            uint8_t msb = (crc >> 7);
            crc <<= 1;
            if(msb)crc ^= 0x2F;
        }
    }
    return crc;
}

uint8_t CALC_CRC8_shift(uint16_t wData){
    uint8_t data[2] = {wData >> 8 , wData & 0xFF};
    uint8_t crc = 0xFF;
    for(int i = 0;i < 2;i++){
        crc ^= data[i];
        for(uint8_t d = 0;d < 8;d++){
            uint8_t msb = (crc >> 7);
            crc <<= 1;
            if(msb)crc ^= 0x2F;
        }
    }
    return crc;
}