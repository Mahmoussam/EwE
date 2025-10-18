#include <stdio.h>
#include <stdint.h>
union Status3
{
    uint16_t Data;            // This defines the length of the union (16bits)
    struct
    {
        uint16_t  Reserved  :6;
        uint16_t  POR_1     :1;
        uint16_t  POR_2     :1;
        uint16_t  FSISO     :1;
        uint16_t  PWM       :1;
        uint16_t  PWMALT    :1;
        uint16_t  FSSTATE   :1;
        uint16_t  FSENB     :1;
        uint16_t  INTB      :1;
        uint16_t  INTA      :1;
        uint16_t  VRTMON    :1;

    } Bits;
};
int main(){
    union Status3 reg;
    reg.Bits.VRTMON = 1;
    printf("%u\n" , reg.Data);

}