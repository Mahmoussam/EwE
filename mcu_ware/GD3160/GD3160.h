/** Endianity differs in unions bit field  LSB/MSB ordering **/
#define LITTLE_ENDIAN

/**
 * @author: Ewise
 * @file GD3160.h
 * @brief 
 *  Based on the driver example provided by NXP
 */

#ifndef GD3160_H
#define GD3160_H

#include <stdint.h>
#include "GD3160_map.h"

/**************************************************************/
// Misc
/**************************************************************/

#define READ  0
#define WRITE 1


// SPI Constants
#define SPI_CHECKSUM_LENGTH  8
#define SPI_CHECKSUM_MASK    0xFF
#define SPI_REG_DATA_MASK    0x3FF
#define SPI_WORD_BYTE_LENGTH 3
#define ALL_STATUS_FAULTS    0x3FF
#define POR_STATUS_FAULTS    0x300

#define FAULT_MASKED 0
#define FAULT_NOT_MASKED 1
#define REPORT_ON_INTB 0
#define REPORT_ON_INTA 1
#define DISABLED 0
#define ENABLED  1
#define AOUT_ONE_SIGNAL  0
#define AOUT_TWO_SIGNALS 1

// SPI read/write error codes
#define SPI_ERROR_STATUS   0xFFFF;
#define SPI_ERROR_BASE     0xFFFFFF00
#define SPI_ERROR_ADDRESS  0xFFFFFFAE
#define SPI_ERROR_CHECKSUM 0xFFFFFFCE

// Status Register 1 Bit Masks
#define STATUS1_IGBT_OVER_CURRENT    0X0001
#define STATUS1_IGBT_SHORT_CIRCUIT   0X0002
#define STATUS1_VCE_DESAT_EVENT      0X0004
#define STATUS1_VCE_CLAMP_EVENT      0X0008
#define STATUS1_IGBT_OVERTEMP_WARN   0X0010
#define STATUS1_IGBT_OVERTEMP_SHUTDN 0X0020
#define STATUS1_DIE_OVERTEMP_SHUTDN  0X0040
#define STATUS1_VSUP_OVER_VOLTAGE    0X0080
#define STATUS1_VCCREG_UNDER_VOLTAGE 0X0100
#define STATUS1_VCC_OVER_VOLTAGE     0X0200

// Status Register 2 Bit Masks
#define STATUS2_VEE_OUT_OF_RANGE     0X0001
#define STATUS2_VREF_OUT_OF_RANGE    0X0002
#define STATUS2_DIE_COMM_ERROR       0X0004
#define STATUS2_WDOG_FAULT           0X0008
#define STATUS2_VGE_FAULT            0X0010
#define STATUS2_CONFIG_CRC_ERROR     0X0020
#define STATUS2_SPI_ERROR            0X0040
#define STATUS2_PWM_DEADTIME_FAULT   0X0080
#define STATUS2_VDD_OUT_OF_RANGE     0X0100
#define STATUS2_BIST_FAILURE         0X0200

// Status Register 3 Bit Masks
#define STATUS3_VRTMON_PIN_STATE     0X0001
#define STATUS3_INTA_PIN_STATE       0X0002
#define STATUS3_INTB_PIN_STATE       0X0004
#define STATUS3_FSENB_PIN_STATE      0X0008
#define STATUS3_FSSTATE_PIN_STATE    0X0010
#define STATUS3_PWMALT_PIN_STATE     0X0020
#define STATUS3_PWM_PIN_STATE        0X0040
#define STATUS3_FSISO_PIN_STATE      0X0080
#define STATUS3_POR2_STATE           0X0100
#define STATUS3_PO12_STATE           0X0200

// Dead Time Settings
#define DEADTIME_0_12_OR_0_06US 0x00
#define DEADTIME_0_20_OR_0_10US 0x01
#define DEADTIME_0_40_OR_0_20US 0x02
#define DEADTIME_0_72_OR_0_36US 0x03
#define DEADTIME_1_00_OR_0_50US 0x04
#define DEADTIME_1_48_OR_0_74US 0x05
#define DEADTIME_2_00_OR_1_00US 0x06
#define DEADTIME_2_48_OR_1_24US 0x07
#define DEADTIME_3_00_OR_1_50US 0x08
#define DEADTIME_3_48_OR_1_74US 0x09
#define DEADTIME_4_00_OR_2_00US 0x0A
#define DEADTIME_4_48_OR_2_24US 0x0B
#define DEADTIME_5_00_OR_2_50US 0x0C
#define DEADTIME_5_48_OR_2_74US 0x0D
#define DEADTIME_6_00_OR_3_00US 0x0E
#define DEADTIME_6_48_OR_3_24US 0x0F

// ReqADC AMUX Values
typedef enum ReqAdcAmux
{
    REQADC_VCCREG         = 0x00,
    REQADC_AMUX           = 0x01,
    REQADC_VCC            = 0x02,
    REQADC_VEE            = 0x03,
    REQADC_PWRDEV_TEMP    = 0x04,
    REQADC_HV_DOMAIN_TEMP = 0x05,
}ReqAdcAmux;

#define MODE2_CONFIG_EN_BIT 0x04
#define MODE2_TISNS_EN_BIT  0x20

// Default power-up register values for GD3160
#define MODE1_DEFAULT_VALUE   0x0F4
#define MODE2_DEFAULT_VALUE   0x260
#define CONFIG1_DEFAULT_VALUE 0x0DB
#define CONFIG2_DEFAULT_VALUE 0x0D4
#define CONFIG3_DEFAULT_VALUE 0x024
#define CONFIG4_DEFAULT_VALUE 0x16B
#define CONFIG5_DEFAULT_VALUE 0x3C6
#define CONFIG6_DEFAULT_VALUE 0x0BA
#define CONFIG7_DEFAULT_VALUE 0x00A
#define CONFIGAOUT_DEFAULT_VALUE 0x300


#define OT_TH_DEFAULT_VALUE 0xFF
#define OTW_TH_DEFAULT_VALUE 0x3FF


// Register Config 1 defines for undervoltage threshold
#define GD_CONF1_UV_TH_10_0V 0x0
#define GD_CONF1_UV_TH_10_5V 0x1
#define GD_CONF1_UV_TH_11_0V 0x2
#define GD_CONF1_UV_TH_11_5V 0x3
#define GD_CONF1_UV_TH_12_0V 0x4
#define GD_CONF1_UV_TH_12_5V 0x5
#define GD_CONF1_UV_TH_13_0V 0x6
#define GD_CONF1_UV_TH_13_5V 0x7

// Register Config 1 defines for overcurrent threshold
#define GD_CONF1_OCTH_0_25V 0x0
#define GD_CONF1_OCTH_0_50V 0x1
#define GD_CONF1_OCTH_0_75V 0x2
#define GD_CONF1_OCTH_1_00V 0x3
#define GD_CONF1_OCTH_1_25V 0x4
#define GD_CONF1_OCTH_1_50V 0x5
#define GD_CONF1_OCTH_1_75V 0x6
#define GD_CONF1_OCTH_2_00V 0x7

// Register Config 1 defines for overcurrent fault filter time
#define GD_CONF1_OCFILT_0_5U 0x0
#define GD_CONF1_OCFILT_1_0U 0x1
#define GD_CONF1_OCFILT_1_5U 0x2
#define GD_CONF1_OCFILT_2_0U 0x3
#define GD_CONF1_OCFILT_2_5U 0x4
#define GD_CONF1_OCFILT_3_0U 0x5
#define GD_CONF1_OCFILT_3_5U 0x6
#define GD_CONF1_OCFILT_4_0U 0x7

// Register Config 2 defines for 2 Level Turn-off voltage (GD3160)
#define GD_CONF2_2LTOV_6_48  0x00
#define GD_CONF2_2LTOV_6_67  0x01
#define GD_CONF2_2LTOV_6_87  0x02
#define GD_CONF2_2LTOV_7_08  0x03
#define GD_CONF2_2LTOV_7_32  0x04
#define GD_CONF2_2LTOV_7_56  0x05
#define GD_CONF2_2LTOV_7_83  0x06
#define GD_CONF2_2LTOV_8_13  0x07
#define GD_CONF2_2LTOV_8_46  0x08
#define GD_CONF2_2LTOV_8_81  0x09
#define GD_CONF2_2LTOV_9_19  0x0A
#define GD_CONF2_2LTOV_9_62  0x0B
#define GD_CONF2_2LTOV_10_09 0x0C
#define GD_CONF2_2LTOV_10_62 0x0D
#define GD_CONF2_2LTOV_11_21 0x0E
#define GD_CONF2_2LTOV_11_88 0x0F


// Register Config 2 defines for Short-circuit threshold voltage
#define GD_CONF2_SCTH_0_50V 0x0
#define GD_CONF2_SCTH_0_75V 0x1
#define GD_CONF2_SCTH_1_00V 0x2
#define GD_CONF2_SCTH_1_25V 0x3
#define GD_CONF2_SCTH_1_50V 0x4
#define GD_CONF2_SCTH_2_00V 0x5
#define GD_CONF2_SCTH_2_50V 0x6
#define GD_CONF2_SCTH_3_00V 0x7

// SCFF=0 SCFF=1
#define GD_CONF2_SCFILT_400_OR_100N  0x0
#define GD_CONF2_SCFILT_500_OR_200N  0x1
#define GD_CONF2_SCFILT_600_OR_300N  0x2
#define GD_CONF2_SCFILT_700_OR_400N  0x3
#define GD_CONF2_SCFILT_800_OR_500N  0x4
#define GD_CONF2_SCFILT_900_OR_600N  0x5
#define GD_CONF2_SCFILT_1000_OR_700N 0x6
#define GD_CONF2_SCFILT_1100_OR_800N 0x7

// Register Config 3 defines for segmented drive activation delay (GD3160)
#define GD_CONF3_SEGDRVDLY_20N  0x0
#define GD_CONF3_SEGDRVDLY_40N  0x1
#define GD_CONF3_SEGDRVDLY_60N  0x2
#define GD_CONF3_SEGDRVDLY_80N  0x3
#define GD_CONF3_SEGDRVDLY_100N 0x4
#define GD_CONF3_SEGDRVDLY_120N 0x5
#define GD_CONF3_SEGDRVDLY_140N 0x6
#define GD_CONF3_SEGDRVDLY_160N 0x7

// Register Config 3 defines for Soft shutdown current
#define GD_CONF3_SSD_CUR_0_1A 0x0
#define GD_CONF3_SSD_CUR_0_2A 0x1
#define GD_CONF3_SSD_CUR_0_3A 0x2
#define GD_CONF3_SSD_CUR_0_4A 0x3
#define GD_CONF3_SSD_CUR_0_6A 0x4
#define GD_CONF3_SSD_CUR_0_8A 0x5
#define GD_CONF3_SSD_CUR_1_0A 0x6
#define GD_CONF3_SSD_CUR_1_2A 0x7

// Register Config 3 defines for Soft shutdown time
#define GD_CONF3_SSDT_2U 0x0
#define GD_CONF3_SSDT_3U 0x1
#define GD_CONF3_SSDT_4U 0x2
#define GD_CONF3_SSDT_5U 0x3
#define GD_CONF3_SSDT_6U 0x4
#define GD_CONF3_SSDT_7U 0x5
#define GD_CONF3_SSDT_8U 0x6
#define GD_CONF3_SSDT_9U 0x7

// Register Config 4 defines for Segmented drive threshold (GD3160)
#define GD_CONF4_SEGDRV_TH_3_0V  0x0
#define GD_CONF4_SEGDRV_TH_4_0V  0x1
#define GD_CONF4_SEGDRV_TH_5_0V  0x2
#define GD_CONF4_SEGDRV_TH_6_0V  0x3 // Default
#define GD_CONF4_SEGDRV_TH_7_0V  0x4
#define GD_CONF4_SEGDRV_TH_8_0V  0x5
#define GD_CONF4_SEGDRV_TH_9_0V  0x6
#define GD_CONF4_SEGDRV_TH_10_0V 0x7

// Register Config 4 defines for Segmented drive threshold (GD3160)
#define GD_CONF4_DESAT_FLT_40N   0x0
#define GD_CONF4_DESAT_FLT_80N   0x1 // Default
#define GD_CONF4_DESAT_FLT_160N  0x2
#define GD_CONF4_DESAT_FLT_300N  0x3

// Register Config 4 defines for Desaturation leading edge blanking time (GD3160)
#define GD_CONF4_DESAT_LEB_60N  0x0
#define GD_CONF4_DESAT_LEB_120N 0x1
#define GD_CONF4_DESAT_LEB_180N 0x2
#define GD_CONF4_DESAT_LEB_240N 0x3
#define GD_CONF4_DESAT_LEB_340N 0x4
#define GD_CONF4_DESAT_LEB_460N 0x5
#define GD_CONF4_DESAT_LEB_480N 0x6
#define GD_CONF4_DESAT_LEB_700N 0x7

// Register Config 4 defines for AOUT_SEL is used for dual AOUT reporting mode (GD3160)
#define GD_CONF4_AOUT_SEL_VCCREG     0x0
#define GD_CONF4_AOUT_SEL_AMUXIN     0x1
#define GD_CONF4_AOUT_SEL_VCC        0x2
#define GD_CONF4_AOUT_SEL_VEE        0x3
#define GD_CONF4_AOUT_SEL_PWRDEVTEMP 0x4
#define GD_CONF4_AOUT_SEL_DIE_TEMP   0x5


// Register Config 4 defines for Charging current for desaturation detection circuitry
#define GD_CONF4_IDESAT_250U  0x0
#define GD_CONF4_IDESAT_500U  0x1
#define GD_CONF4_IDESAT_750U  0x2
#define GD_CONF4_IDESAT_1000U 0x3

// Register Config 7 defines for VCE desaturation threshold (GD3160)
#define GD_CONF7_DESAT_TH_1_0V  0x0
#define GD_CONF7_DESAT_TH_1_5V  0x1
#define GD_CONF7_DESAT_TH_2_0V  0x2
#define GD_CONF7_DESAT_TH_2_5V  0x3
#define GD_CONF7_DESAT_TH_3_0V  0x4
#define GD_CONF7_DESAT_TH_3_5V  0x5
#define GD_CONF7_DESAT_TH_4_0V  0x6
#define GD_CONF7_DESAT_TH_4_5V  0x7
#define GD_CONF7_DESAT_TH_5_0V  0x8
#define GD_CONF7_DESAT_TH_5_5V  0x9
#define GD_CONF7_DESAT_TH_6_0V  0xA
#define GD_CONF7_DESAT_TH_6_5V  0xB
#define GD_CONF7_DESAT_TH_7_0V  0xC
#define GD_CONF7_DESAT_TH_8_0V  0xD
#define GD_CONF7_DESAT_TH_9_0V  0xE
#define GD_CONF7_DESAT_TH_10_0V 0xF


// Register Config 5 defines for Mandatory PWM deadtime
#define GD_CONF5_DEADT_0U50 0x0
#define GD_CONF5_DEADT_0U75 0x1
#define GD_CONF5_DEADT_1U00 0x2
#define GD_CONF5_DEADT_1U25 0x3
#define GD_CONF5_DEADT_1U50 0x4
#define GD_CONF5_DEADT_1U75 0x5
#define GD_CONF5_DEADT_2U00 0x6
#define GD_CONF5_DEADT_2U25 0x7
#define GD_CONF5_DEADT_2U50 0x8
#define GD_CONF5_DEADT_2U75 0x9
#define GD_CONF5_DEADT_3U00 0xA
#define GD_CONF5_DEADT_3U25 0xB
#define GD_CONF5_DEADT_3U50 0xC
#define GD_CONF5_DEADT_3U75 0xD
#define GD_CONF5_DEADT_4U00 0xE
#define GD_CONF5_DEADT_4U25 0xF

// Register Config 5 defines for Number of TEMPSENSE ADC reading vs. AMUX reading
#define GD_CONF5_AOUTCONF_1_1 0x0
#define GD_CONF5_AOUTCONF_1_2 0x1
#define GD_CONF5_AOUTCONF_1_4 0x2
#define GD_CONF5_AOUTCONF_1_8 0x3

// Register Config 5 defines for Number of Die-to-Die communication errors needed to latch a COMERR fault (GD3160)
#define GD_CONF5_COMERRCONF21_4  0x0
#define GD_CONF5_COMERRCONF21_8  0x1
#define GD_CONF5_COMERRCONF21_16 0x2
#define GD_CONF5_COMERRCONF21_32 0x3


// Register Config 5 defines for Number of valid Die-to-Die messages is needed to decrement the error counter
#define GD_CONF5_COMERRCONF0_1 0x0
#define GD_CONF5_COMERRCONF0_4 0x1

// Register Config 3 defines for INTBFS (GD3160)
#define GD_CONF3_INTBFS_FSENB_DIS 0x0
#define GD_CONF3_INTBFS_FSENB_EN  0x1


// Register Config 6 defines for Watchdog timeout
#define GD_CONF6_WDTO_260U  0x0
#define GD_CONF6_WDTO_500U  0x1
#define GD_CONF6_WDTO_1000U 0x2
#define GD_CONF6_WDTO_2000U 0x3 // Default

// Register Config 6 defines for VCCREG voltage (GD3160)
#define GD_CONF6_VCCREG_14_0V 0x0
#define GD_CONF6_VCCREG_15_0V 0x1 // Default
#define GD_CONF6_VCCREG_16_0V 0x2
#define GD_CONF6_VCCREG_17_0V 0x3
#define GD_CONF6_VCCREG_18_0V 0x4
#define GD_CONF6_VCCREG_19_0V 0x5
#define GD_CONF6_VCCREG_20_0V 0x6
#define GD_CONF6_VCCREG_21_0V 0x7

// Register Config 6 defines for PWM versus RT monitor delay (GD3160)
//                        T2=0   T2=1
#define GD_CONF6_RTMONDLY_200_OR_100N   0x0
#define GD_CONF6_RTMONDLY_400_OR_200N   0x1
#define GD_CONF6_RTMONDLY_800_OR_400N   0x2
#define GD_CONF6_RTMONDLY_1200_OR_600N  0x3
#define GD_CONF6_RTMONDLY_1600_OR_800N  0x4
#define GD_CONF6_RTMONDLY_2000_OR_1000N 0x5
#define GD_CONF6_RTMONDLY_2400_OR_1200N 0x6
#define GD_CONF6_RTMONDLY_2800_OR_1400N 0x7
#define GD_CONF6_RTMONDLY_3200_OR_1600N 0x8
#define GD_CONF6_RTMONDLY_3600_OR_1800N 0x9
#define GD_CONF6_RTMONDLY_4000_OR_2000N 0xA // Default
#define GD_CONF6_RTMONDLY_4800_OR_2400N 0xB
#define GD_CONF6_RTMONDLY_5600_OR_2800N 0xC
#define GD_CONF6_RTMONDLY_6400_OR_3200N 0xD
#define GD_CONF6_RTMONDLY_7200_OR_3600N 0xE
#define GD_CONF6_RTMONDLY_8000_OR_4000N 0xF

#define GD_CONFAOUT_ITSNS_0_25MA 0x0
#define GD_CONFAOUT_ITSNS_0_50MA 0x1
#define GD_CONFAOUT_ITSNS_0_75MA 0x2
#define GD_CONFAOUT_ITSNS_1_00MA 0x3 // Default

#define GD_CONFAOUT_TOFST_0_0V 0x0   // Default
#define GD_CONFAOUT_TOFST_0_5V 0x1
#define GD_CONFAOUT_TOFST_1_0V 0x2
#define GD_CONFAOUT_TOFST_1_5V 0x3

#define GD_CONFAOUT_AMUXINOS_0_0V 0x0 // Default
#define GD_CONFAOUT_AMUXINOS_0_5V 0x1
#define GD_CONFAOUT_AMUXINOS_1_0V 0x2
#define GD_CONFAOUT_AMUXINOS_1_5V 0x3

/**************************************************************/
// Enums
/**************************************************************/

#if defined(BIG_ENDIAN) && !defined(LITTLE_ENDIAN)
    
    //===================================================================
    // @brief SPI 24Bit message bit definition for GD3160
    //===================================================================
    typedef union{
        uint32_t Data;
    }SPIMessage;
    //===================================================================
    // @brief Mode1 register bit definition for GD3160
    //===================================================================
    union Mode1
    {
        uint16_t Data;            // This defines the length of the union:16bit
        struct
        {
            uint16_t  Reserved  :6;
            uint16_t  AOUT      :1;
            uint16_t  SEGDRV    :1;
            uint16_t  AMC       :1;
            uint16_t  TIME_2    :1;
            uint16_t  SSD       :1;
            uint16_t  M1_2LTO   :1;
            uint16_t  ACTCLMP   :1;
            uint16_t  DESAT     :1;
            uint16_t  SCSNS     :1;
            uint16_t  OCSNS     :1;

        } Bits;
    };

    //===================================================================
    // @brief Mode2 register bit definition for GD3160
    //===================================================================
    union Mode2
    {
        uint16_t Data;            // This defines the length of the union (16bits)
        struct
        {
            uint16_t  Reserved  :6;
            uint16_t  SCFF      :1;
            uint16_t  RTRPT     :1;
            uint16_t  RTMON     :1;
            uint16_t  FSISOEN   :1;  // FSISO not active, pin state ignored/FSISO pin is active, controls tri-state of gate drive
            uint16_t  TISNS_EN  :1;
            uint16_t  D4        :1;
            uint16_t  BIST      :1;  // BIST feature is not active/Request BIST of LV/HV die. PWMing disable until BIST completed
            uint16_t  CONFIG_EN :1;  // Configuration of SPI register disable/Enable SPI configure register
            uint16_t  RESET     :1;  // GD3100 not in reset/in reset, all configuration register set to default
            uint16_t  D0        :1;

        } Bits;
    };

    //===================================================================
    // @brief Config1 register bit definition for GD3160
    //===================================================================
    union Config1
    {
        uint16_t Data;            // This defines the length of the union (16bits)
        struct
        {
            uint16_t  Reserved  :6;
            uint16_t  UV_LATCH  :1;
            uint16_t  UV_TH     :3;
            uint16_t  OCTH      :3;
            uint16_t  OCFILT    :3;

        } Bits;
    };

    //===================================================================
    // @brief Config2 register bit definition for GD3160
    //===================================================================
    union Config2
    {
        uint16_t Data;            // This defines the length of the union (16bits)
        struct
        {
            uint16_t  Reserved  :6;
            uint16_t  C2_2LTOV  :4;
            uint16_t  SCTH      :3;
            uint16_t  SCFILT    :3;

        } Bits;
    };

    //===================================================================
    // @brief Config3 register bit definition for GD3160
    //===================================================================
    union Config3
    {
        uint16_t Data;            // This defines the length of the union (16bits)
        struct
        {
            uint16_t  Reserved    :6;
            uint16_t  INTBFS      :1;
            uint16_t  SEGDRV_DLY  :3;
            uint16_t  SSD_CUR     :3;
            uint16_t  SSDT        :3;

        } Bits;
    };

    //===================================================================
    // @brief Config4 register bit definition for GD3160
    //===================================================================
    union Config4
    {
        uint16_t Data;            // This defines the length of the union (16bits)
        struct
        {
            uint16_t  Reserved   :6;
            uint16_t  DESAT_FLT  :2;
            uint16_t  SEGDRV_TH  :3;
            uint16_t  IDESAT     :2;
            uint16_t  DESAT_LEB  :3;

        } Bits;
    };

    //===================================================================
    // @brief Config5 register bit definition for GD3160
    //===================================================================
    union Config5
    {
        uint16_t Data;            // This defines the length of the union (16bits)
        struct
        {
            uint16_t  Reserved    :6;
            uint16_t  DEADT       :4;
            uint16_t  D5          :1;
            uint16_t  AOUTCONF    :2;
            uint16_t  COMERRCONF21:2;
            uint16_t  COMERRCONF0 :1;

        } Bits;
    };

    //===================================================================
    // @brief Config6 register bit definition for GD3160
    //===================================================================
    union Config6
    {
        uint16_t Data;            // This defines the length of the union (16bits)
        struct
        {
            uint16_t  Reserved   :6;
            uint16_t  VCCREG     :3;
            uint16_t  D6         :1;
            uint16_t  WDTO       :2;
            uint16_t  RTMONDLY   :4;

        } Bits;
    };

    //===================================================================
    // @brief Config7 register bit definition for GD3160
    //===================================================================
    union Config7
    {
        uint16_t Data;            // This defines the length of the union (16bits)
        struct
        {
            uint16_t  Reserved   :6;
            uint16_t  D9         :1;
            uint16_t  D8         :1;
            uint16_t  D7         :1;
            uint16_t  D6         :1;
            uint16_t  D5         :1;
            uint16_t  D4         :1;
            uint16_t  DESAT_TH   :4;

        } Bits;
    };

    //===================================================================
    // @brief ConfigAout register bit definition for GD3160
    //===================================================================
    union ConfigAout
    {
        uint16_t Data;            // This defines the length of the union (16bits)
        struct
        {
            uint16_t  Reserved   :6;
            uint16_t  ITSNS      :2;
            uint16_t  TOFST      :2;
            uint16_t  TRNG       :1;
            uint16_t  AMUXINRNG  :1;
            uint16_t  AMUXINOS   :2;
            uint16_t  AOUT_SEL   :2;

        } Bits;
    };

    //===================================================================
    // @brief OverTemp Threshold register bit definition for GD3160
    //===================================================================
    union OverTempThresh
    {
        uint16_t Data;            // This defines the length of the union (16bits)
        struct
        {
            uint16_t  Reserved  :6;
            uint16_t  OT_TH     :10;

        } Bits;
    };

    //===================================================================
    // @brief OverTemp Warning Threshold register bit definition for GD3160
    //===================================================================
    union OverTempWarnThresh
    {
        uint16_t Data;            // This defines the length of the union (16bits)
        struct
        {
            uint16_t  Reserved  :6;
            uint16_t  OTW_TH    :10;

        } Bits;
    };

    //===================================================================
    // @brief Status1 register bit definition for GD3160
    //===================================================================
    union Status1
    {
        uint16_t Data;            // This defines the length of the union (16bits)
        struct
        {
            uint16_t  Reserved  :6;
            uint16_t  VCCOV     :1;
            uint16_t  VCCREGUV  :1;
            uint16_t  VSUPOV    :1;
            uint16_t  OTSD_IC   :1;
            uint16_t  OTSD      :1;
            uint16_t  OTW       :1;
            uint16_t  CLAMP     :1;
            uint16_t  DESAT     :1;
            uint16_t  SC        :1;
            uint16_t  OC        :1;

        } Bits;
    };

    //===================================================================
    // @brief StatusMask1 register bit definition for GD3160
    //===================================================================
    union StatusMask1
    {
        uint16_t Data;            // This defines the length of the union (16bits)
        struct
        {
            uint16_t  Reserved  :6;
            uint16_t  VCCOVM    :1;
            uint16_t  VCCREGUVM :1;
            uint16_t  VSUPOVM   :1;
            uint16_t  D6        :1;
            uint16_t  OTSDM     :1;
            uint16_t  OTWM      :1;
            uint16_t  CLAMPM    :1;
            uint16_t  D2        :1;
            uint16_t  D1        :1;
            uint16_t  OCM       :1;

        } Bits;
    };

    //===================================================================
    // @brief ReportMask1 register bit definition for GD3160
    //===================================================================
    union ReportMask1
    {
        uint16_t Data;            // This defines the length of the union (16bits)
        struct
        {
            uint16_t  Reserved  :6;
            uint16_t  VCCOVA    :1;
            uint16_t  VCCREGUVA :1;
            uint16_t  VSUPOVA   :1;
            uint16_t  OTSD_ICA  :1;
            uint16_t  OTSDA     :1;
            uint16_t  OTWA      :1;
            uint16_t  CLAMPA    :1;
            uint16_t  DESATA    :1;
            uint16_t  SCA       :1;
            uint16_t  OCA       :1;

        } Bits;
    };

    //===================================================================
    // @brief Status2 register bit definition for GD3160
    //===================================================================
    union Status2
    {
        uint16_t Data;            // This defines the length of the union (16bits)
        struct
        {
            uint16_t  Reserved   :6;
            uint16_t  BIST_FAIL  :1;
            uint16_t  VDD_UVOV   :1;
            uint16_t  DTFLT      :1;
            uint16_t  SPIERR     :1;
            uint16_t  CONFCRCERR :1;
            uint16_t  PWMON_FLT  :1;
            uint16_t  WDOG_FLT   :1;
            uint16_t  COMERR     :1;
            uint16_t  VREF       :1;
            uint16_t  VEE        :1;

        } Bits;
    };

    //===================================================================
    // @brief StatusMask2 register bit definition for GD3160
    //===================================================================
    union StatusMask2
    {
        uint16_t Data;            // This defines the length of the union (16bits)
        struct
        {
            uint16_t  Reserved    :6;
            uint16_t  D9          :1;
            uint16_t  D8          :1;
            uint16_t  DTFLTM      :1;
            uint16_t  SPIERRM     :1;
            uint16_t  CONFCRCERRM :1;
            uint16_t  RTMON_FLTM  :1;
            uint16_t  WDOG_FLTM   :1;
            uint16_t  COMERRM     :1;
            uint16_t  D1          :1;
            uint16_t  VEE_OORM    :1;

        } Bits;
    };

    //===================================================================
    // @brief ReoportMask2 register bit definition for GD3160
    //===================================================================
    union ReportMask2
    {
        uint16_t Data;            // This defines the length of the union (16bits)
        struct
        {
            uint16_t  Reserved    :6;
            uint16_t  D9          :1;
            uint16_t  D8          :1;
            uint16_t  DTFLTA      :1;
            uint16_t  D6          :1;
            uint16_t  D5          :1;
            uint16_t  D4          :1;
            uint16_t  D3          :1;
            uint16_t  D2          :1;
            uint16_t  VREF_UVA    :1;
            uint16_t  VEE_OORA    :1;

        } Bits;
    };

    //===================================================================
    // @brief Status3 register bit definition for GD3160
    //===================================================================
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

    //===================================================================
    // @brief ADC Request register bit definition for GD3160
    //===================================================================
    union ReqAdc
    {
        uint16_t Data;            // This defines the length of the union (16bits)
        struct
        {
            uint16_t  Reserved  :6;
            uint16_t  D9        :1;
            uint16_t  D8        :1;
            uint16_t  D7        :1;
            uint16_t  D6        :1;
            uint16_t  D5        :1;
            uint16_t  D4        :1;
            uint16_t  AMUX_SEL  :4;

        } Bits;
    };

    //===================================================================
    // @brief ReqBist register bit definition for GD3160
    //===================================================================
    union ReqBist
    {
        uint16_t Data;            // This defines the length of the union:16bit
        struct
        {
            uint16_t  Reserved   :6;
            uint16_t  DATA_INOUT :1;
            uint16_t  LBIST_D1   :1;
            uint16_t  LBIST_D2   :1;
            uint16_t  OSC_FAIL   :1;
            uint16_t  DESAT_COMP :1;
            uint16_t  SCOC       :1;
            uint16_t  OVTP       :1;
            uint16_t  ADC        :1;
            uint16_t  DIE1_PMD   :1;
            uint16_t  DIE2_PMD   :1;

        } Bits;
    };

    //===================================================================
    // @brief DeviceID register bit definition for GD3160
    //===================================================================
    union DeviceID
    {
        uint16_t Data;            // This defines the length of the union:16bit
        struct
        {
            uint16_t  Reserved   :6;
            uint16_t  D9         :1;
            uint16_t  D8         :1;
            uint16_t  VDD3       :1;
            uint16_t  LVDC       :3;
            uint16_t  FS3ST      :1;
            uint16_t  HVDC       :3;

        } Bits;
    };
#elif defined(LITTLE_ENDIAN) && !defined(BIG_ENDIAN)
    //===================================================================
    // @brief Mode1 register bit definition for GD3160 (little-endian ordering)
    //===================================================================
    union Mode1
    {
        uint16_t Data;            // This defines the length of the union:16bit
        struct
        {
            uint16_t  OCSNS     :1;
            uint16_t  SCSNS     :1;
            uint16_t  DESAT     :1;
            uint16_t  ACTCLMP   :1;
            uint16_t  M1_2LTO   :1;
            uint16_t  SSD       :1;
            uint16_t  TIME_2    :1;
            uint16_t  AMC       :1;
            uint16_t  SEGDRV    :1;
            uint16_t  AOUT      :1;
            uint16_t  Reserved  :6;

        } Bits;
    };

    //===================================================================
    // @brief Mode2 register bit definition for GD3160 (little-endian ordering)
    //===================================================================
    union Mode2
    {
        uint16_t Data;            // This defines the length of the union (16bits)
        struct
        {
            uint16_t  D0        :1;
            uint16_t  RESET     :1;  // GD3100 not in reset/in reset, all configuration register set to default
            uint16_t  CONFIG_EN :1;  // Configuration of SPI register disable/Enable SPI configure register
            uint16_t  BIST      :1;  // BIST feature is not active/Request BIST of LV/HV die. PWMing disable until BIST completed
            uint16_t  D4        :1;
            uint16_t  TISNS_EN  :1;
            uint16_t  FSISOEN   :1;  // FSISO not active, pin state ignored/FSISO pin is active, controls tri-state of gate drive
            uint16_t  RTMON     :1;
            uint16_t  RTRPT     :1;
            uint16_t  SCFF      :1;
            uint16_t  Reserved  :6;

        } Bits;
    };

    //===================================================================
    // @brief Config1 register bit definition for GD3160 (little-endian ordering)
    //===================================================================
    union Config1
    {
        uint16_t Data;            // This defines the length of the union (16bits)
        struct
        {
            uint16_t  OCFILT    :3;
            uint16_t  OCTH      :3;
            uint16_t  UV_TH     :3;
            uint16_t  UV_LATCH  :1;
            uint16_t  Reserved  :6;

        } Bits;
    };

    //===================================================================
    // @brief Config2 register bit definition for GD3160 (little-endian ordering)
    //===================================================================
    union Config2
    {
        uint16_t Data;            // This defines the length of the union (16bits)
        struct
        {
            uint16_t  SCFILT    :3;
            uint16_t  SCTH      :3;
            uint16_t  C2_2LTOV  :4;
            uint16_t  Reserved  :6;

        } Bits;
    };

    //===================================================================
    // @brief Config3 register bit definition for GD3160 (little-endian ordering)
    //===================================================================
    union Config3
    {
        uint16_t Data;            // This defines the length of the union (16bits)
        struct
        {
            uint16_t  SSDT        :3;
            uint16_t  SSD_CUR     :3;
            uint16_t  SEGDRV_DLY  :3;
            uint16_t  INTBFS      :1;
            uint16_t  Reserved    :6;

        } Bits;
    };

    //===================================================================
    // @brief Config4 register bit definition for GD3160 (little-endian ordering)
    //===================================================================
    union Config4
    {
        uint16_t Data;            // This defines the length of the union (16bits)
        struct
        {
            uint16_t  DESAT_LEB  :3;
            uint16_t  IDESAT     :2;
            uint16_t  SEGDRV_TH  :3;
            uint16_t  DESAT_FLT  :2;
            uint16_t  Reserved   :6;

        } Bits;
    };

    //===================================================================
    // @brief Config5 register bit definition for GD3160 (little-endian ordering)
    //===================================================================
    union Config5
    {
        uint16_t Data;            // This defines the length of the union (16bits)
        struct
        {
            uint16_t  COMERRCONF0 :1;
            uint16_t  COMERRCONF21:2;
            uint16_t  AOUTCONF    :2;
            uint16_t  D5          :1;
            uint16_t  DEADT       :4;
            uint16_t  Reserved    :6;

        } Bits;
    };

    //===================================================================
    // @brief Config6 register bit definition for GD3160 (little-endian ordering)
    //===================================================================
    union Config6
    {
        uint16_t Data;            // This defines the length of the union (16bits)
        struct
        {
            uint16_t  RTMONDLY   :4;
            uint16_t  WDTO       :2;
            uint16_t  D6         :1;
            uint16_t  VCCREG     :3;
            uint16_t  Reserved   :6;

        } Bits;
    };

    //===================================================================
    // @brief Config7 register bit definition for GD3160 (little-endian ordering)
    //===================================================================
    union Config7
    {
        uint16_t Data;            // This defines the length of the union (16bits)
        struct
        {
            uint16_t  DESAT_TH   :4;
            uint16_t  D4         :1;
            uint16_t  D5         :1;
            uint16_t  D6         :1;
            uint16_t  D7         :1;
            uint16_t  D8         :1;
            uint16_t  D9         :1;
            uint16_t  Reserved   :6;

        } Bits;
    };

    //===================================================================
    // @brief ConfigAout register bit definition for GD3160 (little-endian ordering)
    //===================================================================
    union ConfigAout
    {
        uint16_t Data;            // This defines the length of the union (16bits)
        struct
        {
            uint16_t  AOUT_SEL   :2;
            uint16_t  AMUXINOS   :2;
            uint16_t  AMUXINRNG  :1;
            uint16_t  TRNG       :1;
            uint16_t  TOFST      :2;
            uint16_t  ITSNS      :2;
            uint16_t  Reserved   :6;

        } Bits;
    };

    //===================================================================
    // @brief OverTemp Threshold register bit definition for GD3160 (little-endian ordering)
    //===================================================================
    union OverTempThresh
    {
        uint16_t Data;            // This defines the length of the union (16bits)
        struct
        {
            uint16_t  OT_TH     :10;
            uint16_t  Reserved  :6;

        } Bits;
    };

    //===================================================================
    // @brief OverTemp Warning Threshold register bit definition for GD3160 (little-endian ordering)
    //===================================================================
    union OverTempWarnThresh
    {
        uint16_t Data;            // This defines the length of the union (16bits)
        struct
        {
            uint16_t  OTW_TH    :10;
            uint16_t  Reserved  :6;

        } Bits;
    };

    //===================================================================
    // @brief Status1 register bit definition for GD3160 (little-endian ordering)
    //===================================================================
    union Status1
    {
        uint16_t Data;            // This defines the length of the union (16bits)
        struct
        {
            uint16_t  OC        :1;
            uint16_t  SC        :1;
            uint16_t  DESAT     :1;
            uint16_t  CLAMP     :1;
            uint16_t  OTW       :1;
            uint16_t  OTSD      :1;
            uint16_t  OTSD_IC   :1;
            uint16_t  VSUPOV    :1;
            uint16_t  VCCREGUV  :1;
            uint16_t  VCCOV     :1;
            uint16_t  Reserved  :6;

        } Bits;
    };

    //===================================================================
    // @brief StatusMask1 register bit definition for GD3160 (little-endian ordering)
    //===================================================================
    union StatusMask1
    {
        uint16_t Data;            // This defines the length of the union (16bits)
        struct
        {
            uint16_t  OCM       :1;
            uint16_t  D1        :1;
            uint16_t  D2        :1;
            uint16_t  CLAMPM    :1;
            uint16_t  OTWM      :1;
            uint16_t  OTSDM     :1;
            uint16_t  D6        :1;
            uint16_t  VSUPOVM   :1;
            uint16_t  VCCREGUVM :1;
            uint16_t  VCCOVM    :1;
            uint16_t  Reserved  :6;

        } Bits;
    };

    //===================================================================
    // @brief ReportMask1 register bit definition for GD3160 (little-endian ordering)
    //===================================================================
    union ReportMask1
    {
        uint16_t Data;            // This defines the length of the union (16bits)
        struct
        {
            uint16_t  OCA       :1;
            uint16_t  SCA       :1;
            uint16_t  DESATA    :1;
            uint16_t  CLAMPA    :1;
            uint16_t  OTWA      :1;
            uint16_t  OTSDA     :1;
            uint16_t  OTSD_ICA  :1;
            uint16_t  VSUPOVA   :1;
            uint16_t  VCCREGUVA :1;
            uint16_t  VCCOVA    :1;
            uint16_t  Reserved  :6;

        } Bits;
    };

    //===================================================================
    // @brief Status2 register bit definition for GD3160 (little-endian ordering)
    //===================================================================
    union Status2
    {
        uint16_t Data;            // This defines the length of the union (16bits)
        struct
        {
            uint16_t  VEE        :1;
            uint16_t  VREF       :1;
            uint16_t  COMERR     :1;
            uint16_t  WDOG_FLT   :1;
            uint16_t  PWMON_FLT  :1;
            uint16_t  CONFCRCERR :1;
            uint16_t  SPIERR     :1;
            uint16_t  DTFLT      :1;
            uint16_t  VDD_UVOV   :1;
            uint16_t  BIST_FAIL  :1;
            uint16_t  Reserved   :6;

        } Bits;
    };

    //===================================================================
    // @brief StatusMask2 register bit definition for GD3160 (little-endian ordering)
    //===================================================================
    union StatusMask2
    {
        uint16_t Data;            // This defines the length of the union (16bits)
        struct
        {
            uint16_t  VEE_OORM    :1;
            uint16_t  D1          :1;
            uint16_t  COMERRM     :1;
            uint16_t  WDOG_FLTM   :1;
            uint16_t  RTMON_FLTM  :1;
            uint16_t  CONFCRCERRM :1;
            uint16_t  SPIERRM     :1;
            uint16_t  DTFLTM      :1;
            uint16_t  D8          :1;
            uint16_t  D9          :1;
            uint16_t  Reserved    :6;

        } Bits;
    };

    //===================================================================
    // @brief ReoportMask2 register bit definition for GD3160 (little-endian ordering)
    //===================================================================
    union ReportMask2
    {
        uint16_t Data;            // This defines the length of the union (16bits)
        struct
        {
            uint16_t  VEE_OORA    :1;
            uint16_t  VREF_UVA    :1;
            uint16_t  D2          :1;
            uint16_t  D3          :1;
            uint16_t  D4          :1;
            uint16_t  D5          :1;
            uint16_t  D6          :1;
            uint16_t  DTFLTA      :1;
            uint16_t  D8          :1;
            uint16_t  D9          :1;
            uint16_t  Reserved    :6;

        } Bits;
    };

    //===================================================================
    // @brief Status3 register bit definition for GD3160 (little-endian ordering)
    //===================================================================
    union Status3
    {
        uint16_t Data;            // This defines the length of the union (16bits)
        struct
        {
            uint16_t  VRTMON    :1;
            uint16_t  INTA      :1;
            uint16_t  INTB      :1;
            uint16_t  FSENB     :1;
            uint16_t  FSSTATE   :1;
            uint16_t  PWMALT    :1;
            uint16_t  PWM       :1;
            uint16_t  FSISO     :1;
            uint16_t  POR_2     :1;
            uint16_t  POR_1     :1;
            uint16_t  Reserved  :6;

        } Bits;
    };

    //===================================================================
    // @brief ADC Request register bit definition for GD3160 (little-endian ordering)
    //===================================================================
    union ReqAdc
    {
        uint16_t Data;            // This defines the length of the union (16bits)
        struct
        {
            uint16_t  AMUX_SEL  :4;
            uint16_t  D4        :1;
            uint16_t  D5        :1;
            uint16_t  D6        :1;
            uint16_t  D7        :1;
            uint16_t  D8        :1;
            uint16_t  D9        :1;
            uint16_t  Reserved  :6;

        } Bits;
    };

    //===================================================================
    // @brief ReqBist register bit definition for GD3160 (little-endian ordering)
    //===================================================================
    union ReqBist
    {
        uint16_t Data;            // This defines the length of the union:16bit
        struct
        {
            uint16_t  DIE2_PMD   :1;
            uint16_t  DIE1_PMD   :1;
            uint16_t  ADC        :1;
            uint16_t  OVTP       :1;
            uint16_t  SCOC       :1;
            uint16_t  DESAT_COMP :1;
            uint16_t  OSC_FAIL   :1;
            uint16_t  LBIST_D2   :1;
            uint16_t  LBIST_D1   :1;
            uint16_t  DATA_INOUT :1;
            uint16_t  Reserved   :6;

        } Bits;
    };

    //===================================================================
    // @brief DeviceID register bit definition for GD3160 (little-endian ordering)
    //===================================================================
    union DeviceID
    {
        uint16_t Data;            // This defines the length of the union:16bit
        struct
        {
            uint16_t  HVDC       :3;
            uint16_t  FS3ST      :1;
            uint16_t  LVDC       :3;
            uint16_t  VDD3       :1;
            uint16_t  D8         :1;
            uint16_t  D9         :1;
            uint16_t  Reserved   :6;

        } Bits;
    };
#else
#error Endianity is ambigious
#endif
/**************************************************************/
// Functions prototype
/**************************************************************/


//////////////////////////////////////////////////////////////////////////////////////////
//  Function name: char Calculate_SPI_CRC
//
/// @brief         Calculates the required GD31xx SPI CRC value.
//
/// @param         uint16_t wData - SPI word.
//
/// @return        unsigned char - CRC value.
//////////////////////////////////////////////////////////////////////////////////////////
unsigned char Calculate_SPI_CRC(uint16_t wData);










#endif