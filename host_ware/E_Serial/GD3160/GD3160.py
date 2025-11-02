
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