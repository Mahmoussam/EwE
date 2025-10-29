/**
 * @author: Ewise
 * @file GD3160_map.h
 * @brief Addresses and mappings for GD3160
 *  Based on the driver example provided by NXP.
 */
#ifndef GD3160_MAP_H
#define GD3160_MAP_H

// SPI Control Bits
#define spiCtrlBitsRead 0x000000  // Read write bit is bit 23
#define spiCtrlBitsWrite 0x800000 // Write changes bit 23 to 1

// SPI Register Addresses
#define spiAddrMode1 0x000000
#define spiAddrMode2 0x040000
#define spiAddrConfig1 0x080000
#define spiAddrConfig2 0x0C0000
#define spiAddrConfig3 0x100000
#define spiAddrConfig4 0x140000
#define spiAddrConfig5 0x180000
#define spiAddrConfig6 0x1C0000

#define spiAddrConfig7 0x200000
#define spiAddrOTThresh 0x240000
#define spiAddrOTWThresh 0x280000

#define spiAddrStatus1 0x2C0000
#define spiAddrStatusMask1 0x300000
#define spiAddrRMask1 0x340000
#define spiAddrStatus2 0x380000
#define spiAddrStatusMask2 0x3C0000
#define spiAddrRMask2 0x400000
#define spiAddrStatus3 0x440000
#define spiAddrConfigAout 0x480000
#define spiAddrReqADC 0x4C0000
#define spiAddrReqBIST 0x500000
#define spiAddrDeviceID 0x540000

#define spiAddrMax spiAddrDeviceID


#define mode2ResetBit        0x02
#define mode2ConfigEnableBit 0x04
#define mode2BistBit         0x08

#endif