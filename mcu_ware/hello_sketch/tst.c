// Author name: Mahmoud
// Date: 10/18/2025
// Day: Saturday


#include <stdio.h>
#include <stdint.h>
union Mode1
{
    unsigned short Data;            // This defines the length of the union:16bit
    struct
    {
        unsigned short  Reserved  :6;
        unsigned short  AOUT      :1;
        unsigned short  SEGDRV    :1;
        unsigned short  AMC       :1;
        unsigned short  TIME_2    :1;
        unsigned short  SSD       :1;
        unsigned short  M1_2LTO   :1;
        unsigned short  ACTCLMP   :1;
        unsigned short  DESAT     :1;
        unsigned short  SCSNS     :1;
        unsigned short  OCSNS     :1;

    } Bits;
};
int main(){
    union Mode1 reg;
    reg.Data = 0x0F4;
    reg.Bits.DESAT = 0;
    printf("0x%0X\n" , reg.Data);

}