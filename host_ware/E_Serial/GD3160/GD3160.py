"""
GD3160 Gate Driver Register Definitions and Mappings
"""

from dataclasses import dataclass, field
from typing import List


@dataclass
class BitDefinition:
    """Definition of a single bit in a register."""

    name: str
    position: int
    description: str = ""
    default: int = 0


@dataclass
class RegisterDefinition:
    """Definition of a GD3160 register."""

    name: str
    address: int  # Hex address
    description: str
    bits: List[BitDefinition] = field(default_factory=list)
    default_value: int = 0

    def get_bit_count(self) -> int:
        return len(self.bits)


# ============================================================================
# GD3160 Register Map - Based on NXP Datasheet Default Values
# ============================================================================

GD3160_REGISTERS: List[RegisterDefinition] = [
    # MODE1 (0x00) - Default: 0x000
    RegisterDefinition(
        name="MODE1",
        address=0x00,
        description="Mode Configuration Register 1 - Enable/disable major functions",
        bits=[
            BitDefinition("AOUT", 9, "Analog Output Select (0=single, 1=dual signal)", 0),
            BitDefinition("SEGDRV", 8, "Segment Driver Enable", 0),
            BitDefinition("AMC", 7, "Active Miller Clamp Enable", 0),
            BitDefinition("TIME_2", 6, "Timing Configuration Bit 2", 0),
            BitDefinition("SSD", 5, "Soft Shutdown Enable", 0),
            BitDefinition("2LTO", 4, "Two-Level Turn-Off Enable", 0),
            BitDefinition("ACTCLMP", 3, "Active Clamp Enable", 0),
            BitDefinition("DESAT", 2, "Desaturation Detection Enable", 0),
            BitDefinition("SCSNS", 1, "Short Circuit Sense Enable", 0),
            BitDefinition("OCSNS", 0, "Over Current Sense Enable", 0),
        ],
        default_value=0x000
    ),
    
    # MODE2 (0x01) - Default: 0x000
    RegisterDefinition(
        name="MODE2",
        address=0x01,
        description="Mode Configuration Register 2 - Critical features control",
        bits=[
            BitDefinition("SCFF", 9, "Short Circuit Fault Filter", 0),
            BitDefinition("RTRPT", 8, "Retry/Repeat Mode", 0),
            BitDefinition("RTMON_CFG", 7, "Real-Time Monitor Config", 0),
            BitDefinition("FSISOEN", 6, "Fail-Safe Isolation Enable", 0),
            BitDefinition("TISNS_EN", 5, "Temperature Sense Enable", 0),
            BitDefinition("BIST", 4, "Built-In Self Test", 0),
            BitDefinition("CONFIG_EN", 3, "Configuration Enable", 0),
            BitDefinition("RESET", 2, "Software Reset", 0),
            BitDefinition("RES1", 1, "Reserved Bit 1", 0),
            BitDefinition("RES0", 0, "Reserved Bit 0", 0),
        ],
        default_value=0x000
    ),
    
    # CONFIG1 (0x02) - Default: 0x000
    RegisterDefinition(
        name="CONFIG1",
        address=0x02,
        description="UV/OC Thresholds Configuration",
        bits=[
            BitDefinition("UV_LATCH", 9, "UV Latch Enable (0=non-latching, 1=latching)", 0),
            BitDefinition("UV_TH[2]", 8, "UV Threshold Bit 2", 0),
            BitDefinition("UV_TH[1]", 7, "UV Threshold Bit 1", 0),
            BitDefinition("UV_TH[0]", 6, "UV Threshold Bit 0", 0),
            BitDefinition("OCTH[2]", 5, "OC Threshold Bit 2", 0),
            BitDefinition("OCTH[1]", 4, "OC Threshold Bit 1", 0),
            BitDefinition("OCTH[0]", 3, "OC Threshold Bit 0", 0),
            BitDefinition("OCFILT[2]", 2, "OC Filter Bit 2", 0),
            BitDefinition("OCFILT[1]", 1, "OC Filter Bit 1", 0),
            BitDefinition("OCFILT[0]", 0, "OC Filter Bit 0", 0),
        ],
        default_value=0x000
    ),
    
    # CONFIG2 (0x03) - Default: 0x088
    RegisterDefinition(
        name="CONFIG2",
        address=0x03,
        description="SC Thresholds and 2-Level Turn-Off Configuration",
        bits=[
            BitDefinition("2LTOV[3]", 9, "2-Level TOV Bit 3", 0),
            BitDefinition("2LTOV[2]", 8, "2-Level TOV Bit 2", 0),
            BitDefinition("2LTOV[1]", 7, "2-Level TOV Bit 1", 1),
            BitDefinition("2LTOV[0]", 6, "2-Level TOV Bit 0", 0),
            BitDefinition("SCTH[2]", 5, "SC Threshold Bit 2", 0),
            BitDefinition("SCTH[1]", 4, "SC Threshold Bit 1", 0),
            BitDefinition("SCTH[0]", 3, "SC Threshold Bit 0", 1),
            BitDefinition("SCFILT[2]", 2, "SC Filter Bit 2", 0),
            BitDefinition("SCFILT[1]", 1, "SC Filter Bit 1", 0),
            BitDefinition("SCFILT[0]", 0, "SC Filter Bit 0", 0),
        ],
        default_value=0x088
    ),
    
    # CONFIG3 (0x04) - Default: 0x000
    RegisterDefinition(
        name="CONFIG3",
        address=0x04,
        description="SSD/Segment Drive Settings",
        bits=[
            BitDefinition("INTBFS", 9, "Internal Bias FS", 0),
            BitDefinition("SEGDRVLDLY[2]", 8, "Segment Drive LDLY Bit 2", 0),
            BitDefinition("SEGDRVLDLY[1]", 7, "Segment Drive LDLY Bit 1", 0),
            BitDefinition("SEGDRVLDLY[0]", 6, "Segment Drive LDLY Bit 0", 0),
            BitDefinition("SSD_CUR[2]", 5, "SSD Current Bit 2", 0),
            BitDefinition("SSD_CUR[1]", 4, "SSD Current Bit 1", 0),
            BitDefinition("SSD_CUR[0]", 3, "SSD Current Bit 0", 0),
            BitDefinition("SSDT[2]", 2, "SSD Timing Bit 2", 0),
            BitDefinition("SSDT[1]", 1, "SSD Timing Bit 1", 0),
            BitDefinition("SSDT[0]", 0, "SSD Timing Bit 0", 0),
        ],
        default_value=0x000
    ),
    
    # CONFIG4 (0x05) - Default: 0x000
    RegisterDefinition(
        name="CONFIG4",
        address=0x05,
        description="Desaturation Settings",
        bits=[
            BitDefinition("RES4_9", 9, "Reserved", 0),
            BitDefinition("DESAT_FLT[1]", 8, "Desat Filter Bit 1", 0),
            BitDefinition("DESAT_FLT[0]", 7, "Desat Filter Bit 0", 0),
            BitDefinition("SEGDRV_TH[2]", 6, "Segment Drive Threshold Bit 2", 0),
            BitDefinition("SEGDRV_TH[1]", 5, "Segment Drive Threshold Bit 1", 0),
            BitDefinition("SEGDRV_TH[0]", 4, "Segment Drive Threshold Bit 0", 0),
            BitDefinition("IDE_SAT[1]", 3, "Desat Current Bit 1", 0),
            BitDefinition("IDE_SAT[0]", 2, "Desat Current Bit 0", 0),
            BitDefinition("DESAT_LEB[2]", 1, "Desat LEB Bit 2", 0),
            BitDefinition("DESAT_LEB[1]", 0, "Desat LEB Bit 1", 0),
        ],
        default_value=0x000
    ),
    
    # CONFIG5 (0x06) - Default: 0x000
    RegisterDefinition(
        name="CONFIG5",
        address=0x06,
        description="Dead Time and AOUT Configuration",
        bits=[
            BitDefinition("RES5_9", 9, "Reserved", 0),
            BitDefinition("DEADT[3]", 8, "Dead Time Bit 3", 0),
            BitDefinition("DEADT[2]", 7, "Dead Time Bit 2", 0),
            BitDefinition("DEADT[1]", 6, "Dead Time Bit 1", 0),
            BitDefinition("DEADT[0]", 5, "Dead Time Bit 0", 0),
            BitDefinition("AOUTCONF[1]", 4, "AOUT Config Bit 1", 0),
            BitDefinition("AOUTCONF[0]", 3, "AOUT Config Bit 0", 0),
            BitDefinition("COMERRCONF[1]", 2, "COM Error Config Bit 1", 0),
            BitDefinition("COMERRCONF[0]", 1, "COM Error Config Bit 0", 0),
            BitDefinition("RES5_0", 0, "Reserved", 0),
        ],
        default_value=0x000
    ),
    
    # CONFIG6 (0x07) - Default: 0x010
    RegisterDefinition(
        name="CONFIG6",
        address=0x07,
        description="VCC Regulation and Watchdog Settings",
        bits=[
            BitDefinition("VCCREG[2]", 9, "VCC Regulation Bit 2", 0),
            BitDefinition("VCCREG[1]", 8, "VCC Regulation Bit 1", 0),
            BitDefinition("VCCREG[0]", 7, "VCC Regulation Bit 0", 0),
            BitDefinition("WDTO[1]", 6, "Watchdog Timeout Bit 1", 0),
            BitDefinition("WDTO[0]", 5, "Watchdog Timeout Bit 0", 0),
            BitDefinition("RTMONDLY[3]", 4, "RTMON Delay Bit 3", 1),
            BitDefinition("RTMONDLY[2]", 3, "RTMON Delay Bit 2", 0),
            BitDefinition("RTMONDLY[1]", 2, "RTMON Delay Bit 1", 0),
            BitDefinition("RTMONDLY[0]", 1, "RTMON Delay Bit 0", 0),
            BitDefinition("RES6_0", 0, "Reserved", 0),
        ],
        default_value=0x010
    ),
    
    # CONFIG7 (0x08) - Default: 0x000
    RegisterDefinition(
        name="CONFIG7",
        address=0x08,
        description="Desaturation Threshold Configuration",
        bits=[
            BitDefinition("DESAT_TH[3]", 9, "Desat Threshold Bit 3", 0),
            BitDefinition("DESAT_TH[2]", 8, "Desat Threshold Bit 2", 0),
            BitDefinition("DESAT_TH[1]", 7, "Desat Threshold Bit 1", 0),
            BitDefinition("DESAT_TH[0]", 6, "Desat Threshold Bit 0", 0),
            BitDefinition("RES7_5", 5, "Reserved", 0),
            BitDefinition("RES7_4", 4, "Reserved", 0),
            BitDefinition("RES7_3", 3, "Reserved", 0),
            BitDefinition("RES7_2", 2, "Reserved", 0),
            BitDefinition("RES7_1", 1, "Reserved", 0),
            BitDefinition("RES7_0", 0, "Reserved", 0),
        ],
        default_value=0x000
    ),
    
    # OT_TH (0x09) - Default: 0x0FF
    RegisterDefinition(
        name="OT_TH",
        address=0x09,
        description="Overtemperature Threshold - Sets threshold for power device OT event (permanently unlocked)",
        bits=[
            BitDefinition("OT_TH[9]", 9, "OT Threshold Bit 9", 0),
            BitDefinition("OT_TH[8]", 8, "OT Threshold Bit 8", 0),
            BitDefinition("OT_TH[7]", 7, "OT Threshold Bit 7", 1),
            BitDefinition("OT_TH[6]", 6, "OT Threshold Bit 6", 1),
            BitDefinition("OT_TH[5]", 5, "OT Threshold Bit 5", 1),
            BitDefinition("OT_TH[4]", 4, "OT Threshold Bit 4", 1),
            BitDefinition("OT_TH[3]", 3, "OT Threshold Bit 3", 1),
            BitDefinition("OT_TH[2]", 2, "OT Threshold Bit 2", 1),
            BitDefinition("OT_TH[1]", 1, "OT Threshold Bit 1", 1),
            BitDefinition("OT_TH[0]", 0, "OT Threshold Bit 0", 1),
        ],
        default_value=0x0FF
    ),
    
    # OTW_TH (0x0A) - Default: 0x3FF
    RegisterDefinition(
        name="OTW_TH",
        address=0x0A,
        description="Overtemperature Warning Threshold - Sets threshold for power device OT warning (permanently unlocked)",
        bits=[
            BitDefinition("OTW_TH[9]", 9, "OTW Threshold Bit 9", 1),
            BitDefinition("OTW_TH[8]", 8, "OTW Threshold Bit 8", 1),
            BitDefinition("OTW_TH[7]", 7, "OTW Threshold Bit 7", 1),
            BitDefinition("OTW_TH[6]", 6, "OTW Threshold Bit 6", 1),
            BitDefinition("OTW_TH[5]", 5, "OTW Threshold Bit 5", 1),
            BitDefinition("OTW_TH[4]", 4, "OTW Threshold Bit 4", 1),
            BitDefinition("OTW_TH[3]", 3, "OTW Threshold Bit 3", 1),
            BitDefinition("OTW_TH[2]", 2, "OTW Threshold Bit 2", 1),
            BitDefinition("OTW_TH[1]", 1, "OTW Threshold Bit 1", 1),
            BitDefinition("OTW_TH[0]", 0, "OTW Threshold Bit 0", 1),
        ],
        default_value=0x3FF
    ),
    
    # STATUS1 (0x0B) - Default: 0x000
    RegisterDefinition(
        name="STATUS1",
        address=0x0B,
        description="Status Register 1 - Fault status (write 1 to clear latched faults)",
        bits=[
            BitDefinition("VCCOV", 9, "VCC overvoltage", 0),
            BitDefinition("VCCREGUV", 8, "VCCREG undervoltage", 0),
            BitDefinition("VSUPOV", 7, "VSUP overvoltage", 0),
            BitDefinition("OTSD_IC", 6, "Overtemperature shutdown of LV/HV domain", 0),
            BitDefinition("OTSD", 5, "Overtemperature shutdown of IGBT", 0),
            BitDefinition("OTW", 4, "Overtemperature warning of IGBT", 0),
            BitDefinition("CLAMP", 3, "VCE clamp event", 0),
            BitDefinition("DESAT", 2, "VCE desaturation event", 0),
            BitDefinition("SC", 1, "IGBT short-circuit", 0),
            BitDefinition("OC", 0, "IGBT overcurrent", 0),
        ],
        default_value=0x000
    ),
    
    # MSK1 (0x0C) - Default: 0x309
    RegisterDefinition(
        name="MSK1",
        address=0x0C,
        description="Status Mask Register 1 - Determines which STATUS1 faults are reported (0=masked, 1=unmasked)",
        bits=[
            BitDefinition("VCCOVM", 9, "VCC overvoltage mask", 1),
            BitDefinition("VCCREGUVM", 8, "VCCREG undervoltage mask", 1),
            BitDefinition("VSUPOVM", 7, "VSUP overvoltage mask", 0),
            BitDefinition("RES6", 6, "Reserved", 0),
            BitDefinition("OTSDM", 5, "Overtemperature shutdown mask", 0),
            BitDefinition("OTWM", 4, "Overtemperature warning mask", 0),
            BitDefinition("CLAMPM", 3, "Clamp mask", 1),
            BitDefinition("RES2", 2, "Reserved", 0),
            BitDefinition("RES1", 1, "Reserved", 0),
            BitDefinition("OCM", 0, "Overcurrent mask", 1),
        ],
        default_value=0x309
    ),
    
    # RMSK1 (0x0D) - Default: 0x0D0
    RegisterDefinition(
        name="RMSK1",
        address=0x0D,
        description="Report Mask Register 1 - Determines interrupt pin allocation (0=INTB, 1=INTA)",
        bits=[
            BitDefinition("VCCOVA", 9, "VCC overvoltage report allocation", 0),
            BitDefinition("VCCREGUVA", 8, "VCCREG undervoltage report allocation", 0),
            BitDefinition("VSUPOVA", 7, "VSUP overvoltage report allocation", 1),
            BitDefinition("OTSD_ICA", 6, "IC overtemperature shutdown report allocation", 1),
            BitDefinition("OTSDA", 5, "IGBT overtemperature shutdown report allocation", 0),
            BitDefinition("OTWA", 4, "Overtemperature warning report allocation", 1),
            BitDefinition("CLAMPA", 3, "Clamp report allocation", 0),
            BitDefinition("DESATA", 2, "Desaturation report allocation", 0),
            BitDefinition("SCA", 1, "Short circuit report allocation", 0),
            BitDefinition("OCA", 0, "Overcurrent report allocation", 0),
        ],
        default_value=0x0D0
    ),
    
    # STATUS2 (0x0E) - Default: 0x000
    RegisterDefinition(
        name="STATUS2",
        address=0x0E,
        description="Status Register 2 - System-level fault status (write 1 to clear latched faults)",
        bits=[
            BitDefinition("BIST_FAIL", 9, "BIST failure", 0),
            BitDefinition("VDD_UVOV", 8, "VDD out of range", 0),
            BitDefinition("DTFLT", 7, "PWM deadtime violation", 0),
            BitDefinition("SPIERR", 6, "SPI framing or CRC error", 0),
            BitDefinition("CONFCRCERR", 5, "Config register CRC error", 0),
            BitDefinition("RTMON_FLT", 4, "Real-time monitor fault", 0),
            BitDefinition("WDOG_FLT", 3, "Watchdog fault", 0),
            BitDefinition("COMERR", 2, "LV/HV domain communication error", 0),
            BitDefinition("VREF_UV", 1, "VREF undervoltage", 0),
            BitDefinition("VEE_OOR", 0, "VEE out of range", 0),
        ],
        default_value=0x000
    ),
    
    # MSK2 (0x0F) - Default: 0x0EC
    RegisterDefinition(
        name="MSK2",
        address=0x0F,
        description="Status Mask Register 2 - Determines which STATUS2 faults are reported (0=masked, 1=unmasked)",
        bits=[
            BitDefinition("RES9", 9, "Reserved", 0),
            BitDefinition("RES8", 8, "Reserved", 0),
            BitDefinition("DTFLTM", 7, "Deadtime fault mask", 1),
            BitDefinition("SPIERRM", 6, "SPI error mask", 1),
            BitDefinition("CONFCRCERRM", 5, "Config CRC error mask", 1),
            BitDefinition("RTMON_FLTM", 4, "Real-time monitor fault mask", 0),
            BitDefinition("WDOG_FLTM", 3, "Watchdog fault mask", 1),
            BitDefinition("COMERRM", 2, "Communication error mask", 1),
            BitDefinition("RES1", 1, "Reserved", 0),
            BitDefinition("VEE_OORM", 0, "VEE out of range mask", 0),
        ],
        default_value=0x0EC
    ),
    
    # RMSK2 (0x10) - Default: 0x002
    RegisterDefinition(
        name="RMSK2",
        address=0x10,
        description="Report Mask Register 2 - Determines interrupt pin allocation for STATUS2 (0=INTB, 1=INTA)",
        bits=[
            BitDefinition("RES9", 9, "Reserved", 0),
            BitDefinition("RES8", 8, "Reserved", 0),
            BitDefinition("DTFLTA", 7, "Deadtime fault report allocation", 0),
            BitDefinition("RES6", 6, "Reserved", 0),
            BitDefinition("RES5", 5, "Reserved", 0),
            BitDefinition("RES4", 4, "Reserved", 0),
            BitDefinition("RES3", 3, "Reserved", 0),
            BitDefinition("RES2", 2, "Reserved", 0),
            BitDefinition("VREF_UVA", 1, "VREF undervoltage report allocation", 1),
            BitDefinition("VEE_OORA", 0, "VEE out of range report allocation", 0),
        ],
        default_value=0x002
    ),
    
    # STATUS3 (0x11) - Default: 0x300
    RegisterDefinition(
        name="STATUS3",
        address=0x11,
        description="Status Register 3 - Reports critical GD3160 control/status pin states after deglitch",
        bits=[
            BitDefinition("POR_1", 9, "LV die power-on reset recovery notification", 1),
            BitDefinition("POR_2", 8, "HV die power-on reset recovery notification", 1),
            BitDefinition("FSISO", 7, "FSISO pin state", 0),
            BitDefinition("PWM", 6, "PWM pin state", 0),
            BitDefinition("PWMALT", 5, "PWMALT pin state", 0),
            BitDefinition("FSSTATE", 4, "FSSTATE pin state", 0),
            BitDefinition("FSENB", 3, "FSENB pin state", 0),
            BitDefinition("INTB", 2, "INTB pin state", 0),
            BitDefinition("INTA", 1, "INTA pin state", 0),
            BitDefinition("VRTMON", 0, "Real-time monitor state (VGE or VCE)", 0),
        ],
        default_value=0x300
    ),
    
    # CONFIGAOUT (0x12) - Default: 0x000
    RegisterDefinition(
        name="CONFIGAOUT",
        address=0x12,
        description="Analog Output Selection Configuration",
        bits=[
            BitDefinition("AOUT_SEL[3]", 9, "AOUT Select Bit 3", 0),
            BitDefinition("AOUT_SEL[2]", 8, "AOUT Select Bit 2", 0),
            BitDefinition("AOUT_SEL[1]", 7, "AOUT Select Bit 1", 0),
            BitDefinition("AOUT_SEL[0]", 6, "AOUT Select Bit 0", 0),
            BitDefinition("RES_5", 5, "Reserved", 0),
            BitDefinition("RES_4", 4, "Reserved", 0),
            BitDefinition("RES_3", 3, "Reserved", 0),
            BitDefinition("RES_2", 2, "Reserved", 0),
            BitDefinition("RES_1", 1, "Reserved", 0),
            BitDefinition("RES_0", 0, "Reserved", 0),
        ],
        default_value=0x000
    ),
    
    # REQADC (0x13) - ADC Request/Response Register
    RegisterDefinition(
        name="REQADC",
        address=0x13,
        description="ADC Request/Response - Write AMUX_SEL to request conversion, read returns 10-bit ADC result",
        bits=[
            BitDefinition("ADCVAL[9]/RES", 9, "ADC Result Bit 9 (read) / Reserved (write)", 0),
            BitDefinition("ADCVAL[8]/RES", 8, "ADC Result Bit 8 (read) / Reserved (write)", 0),
            BitDefinition("ADCVAL[7]/RES", 7, "ADC Result Bit 7 (read) / Reserved (write)", 0),
            BitDefinition("ADCVAL[6]/RES", 6, "ADC Result Bit 6 (read) / Reserved (write)", 0),
            BitDefinition("ADCVAL[5]/RES", 5, "ADC Result Bit 5 (read) / Reserved (write)", 0),
            BitDefinition("ADCVAL[4]/RES", 4, "ADC Result Bit 4 (read) / Reserved (write)", 0),
            BitDefinition("ADCVAL[3]/AMUX_SEL[3]", 3, "ADC Result Bit 3 (read) / AMUX Select Bit 3 (write)", 0),
            BitDefinition("ADCVAL[2]/AMUX_SEL[2]", 2, "ADC Result Bit 2 (read) / AMUX Select Bit 2 (write)", 0),
            BitDefinition("ADCVAL[1]/AMUX_SEL[1]", 1, "ADC Result Bit 1 (read) / AMUX Select Bit 1 (write)", 0),
            BitDefinition("ADCVAL[0]/AMUX_SEL[0]", 0, "ADC Result Bit 0 (read) / AMUX Select Bit 0 (write)", 0),
        ],
        default_value=0x000
    ),
    
    # REQBIST (0x14) - BIST Request/Result Register
    RegisterDefinition(
        name="REQBIST",
        address=0x14,
        description="BIST Request/Result - Read returns BIST status (0=pass, 1=fail for each bit)",
        bits=[
            BitDefinition("DATA_LINK", 9, "DATA_IN/DATA_OUT comm link failure", 0),
            BitDefinition("LV_LBIST", 8, "LV domain LBIST failure", 0),
            BitDefinition("HV_LBIST", 7, "HV domain LBIST failure", 0),
            BitDefinition("OSC_FAIL", 6, "Oscillator failure", 0),
            BitDefinition("DESAT_CMP", 5, "DESAT/SEGDRV comparator failure", 0),
            BitDefinition("ISENSE_CMP", 4, "ISENSE SC/OC comparator failure", 0),
            BitDefinition("OTP_FAIL", 3, "Overtemperature protection failure", 0),
            BitDefinition("ADC_FAIL", 2, "ADC failure", 0),
            BitDefinition("LV_PWR", 1, "LV domain power management failure", 0),
            BitDefinition("HV_PWR", 0, "HV domain power management failure", 0),
        ],
        default_value=0x000
    ),
    
    # ID (0x15) - Device ID Register (Read-Only)
    RegisterDefinition(
        name="ID",
        address=0x15,
        description="Device ID - Provides revision and version info for LV/HV die, VDD selection, FSISO config (Read-Only)",
        bits=[
            BitDefinition("RES9", 9, "Reserved", 0),
            BitDefinition("RES8", 8, "Reserved", 0),
            BitDefinition("VDD3", 7, "VDD selection (0=3.3V, 1=5V)", 0),
            BitDefinition("LVDC[2]", 6, "LV die revision bit 2", 0),
            BitDefinition("LVDC[1]", 5, "LV die revision bit 1", 0),
            BitDefinition("LVDC[0]", 4, "LV die revision bit 0", 0),
            BitDefinition("FS3ST", 3, "FSISO mode (0=On state, 1=3-state)", 0),
            BitDefinition("HVDC[2]", 2, "HV die revision bit 2", 0),
            BitDefinition("HVDC[1]", 1, "HV die revision bit 1", 0),
            BitDefinition("HVDC[0]", 0, "HV die revision bit 0", 0),
        ],
        default_value=0x000
    ),
]


# ============================================================================
# Legacy Register Name Mappings (for backward compatibility)
# ============================================================================

GD3160_REGISTERS_TO_ADDR = {
    "mode1"      : 0x00,
    "mode2"      : 0x01,
    "config1"    : 0x02,
    "config2"    : 0x03,
    "config3"    : 0x04,
    "config4"    : 0x05,
    "config5"    : 0x06,
    "config6"    : 0x07,
    "config7"    : 0x08,
    "ot_th"      : 0x09,
    "otw_th"     : 0x0A,
    "status1"    : 0x0B,
    "msk1"       : 0x0C,
    "rmsk1"      : 0x0D,
    "status2"    : 0x0E,
    "msk2"       : 0x0F,
    "rmsk2"      : 0x10,
    "status3"    : 0x11,
    "configaout" : 0x12,
    "reqadc"     : 0x13,
    "bist"       : 0x14,
    "reqbist"    : 0x14,
    "id"         : 0x15
}
GD3160_ADDR_TO_REGISTERS = {
    0x00: "mode1",
    0x01: "mode2",
    0x02: "config1",
    0x03: "config2",
    0x04: "config3",
    0x05: "config4",
    0x06: "config5",
    0x07: "config6",
    0x08: "config7",
    0x09: "ot_th",
    0x0A: "otw_th",
    0x0B: "status1",
    0x0C: "msk1",
    0x0D: "rmsk1",
    0x0E: "status2",
    0x0F: "msk2",
    0x10: "rmsk2",
    0x11: "status3",
    0x12: "configaout",
    0x13: "reqadc",
    0x14: "reqbist",  
    0x15: "id",
}
def str_to_register3160_addr(register : str) -> int:
    name = register.lower().strip()
    return GD3160_REGISTERS_TO_ADDR[name]

def addr_to_register3160_name(addr : int) -> str:
    return GD3160_ADDR_TO_REGISTERS[addr]