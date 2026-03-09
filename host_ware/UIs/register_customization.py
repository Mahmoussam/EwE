"""
GD3160 Register Customization Helper Module
Provides utilities for dynamically adding/modify registers and bit names

This module allows you to:
- Add new registers to the existing map
- Modify bit names and descriptions
- Import/export register configurations
- Create custom register definitions
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
import json
from pathlib import Path

# Import register models and default GD3160 register list
from E_Serial.GD3160.GD3160 import BitDefinition, RegisterDefinition, GD3160_REGISTERS


class RegisterManager:
    """
    Manager class for dynamically managing GD3160 registers.
    Supports adding, modifying, and removing registers.
    """
    
    def __init__(self):
        self._registers: Dict[str, RegisterDefinition] = {}
        self._load_default_registers()
        
    def _load_default_registers(self):
        """Load default GD3160 registers"""
        for reg in GD3160_REGISTERS:
            self._registers[reg.name] = reg
            
    def get_register(self, name: str) -> Optional[RegisterDefinition]:
        """Get a register by name"""
        return self._registers.get(name)
        
    def get_all_registers(self) -> List[RegisterDefinition]:
        """Get all registers as a list"""
        return list(self._registers.values())
        
    def add_register(self, register: RegisterDefinition):
        """Add a new register or update existing one"""
        self._registers[register.name] = register
        
    def remove_register(self, name: str) -> bool:
        """Remove a register by name. Returns True if removed."""
        if name in self._registers:
            del self._registers[name]
            return True
        return False
        
    def create_register(
        self,
        name: str,
        address: int,
        description: str = "",
        bit_names: List[str] = None,
        bit_descriptions: List[str] = None,
        default_value: int = 0
    ) -> RegisterDefinition:
        """
        Create a new register with automatic bit naming.
        
        Args:
            name: Register name (e.g., "CONFIG8")
            address: Register address in hex
            description: Register description
            bit_names: List of 10 bit names (LSB first)
            bit_descriptions: List of 10 bit descriptions
            default_value: Default register value
            
        Returns:
            The created RegisterDefinition
        """
        bits = []
        for i in range(10):
            bit_name = bit_names[i] if bit_names and i < len(bit_names) else f"BIT{i}"
            bit_desc = bit_descriptions[i] if bit_descriptions and i < len(bit_descriptions) else f"Bit {i}"
            bits.append(BitDefinition(bit_name, i, bit_desc, (default_value >> i) & 1))
            
        register = RegisterDefinition(name, address, description, bits, default_value)
        self.add_register(register)
        return register
        
    def modify_bit_name(self, register_name: str, bit_position: int, new_name: str) -> bool:
        """Modify a bit name in a register"""
        reg = self._registers.get(register_name)
        if reg and 0 <= bit_position < len(reg.bits):
            reg.bits[bit_position].name = new_name
            return True
        return False
        
    def modify_bit_description(self, register_name: str, bit_position: int, new_desc: str) -> bool:
        """Modify a bit description in a register"""
        reg = self._registers.get(register_name)
        if reg and 0 <= bit_position < len(reg.bits):
            reg.bits[bit_position].description = new_desc
            return True
        return False
        
    def export_to_json(self, filepath: str):
        """Export register configuration to JSON file"""
        data = {
            "registers": [
                {
                    "name": reg.name,
                    "address": reg.address,
                    "description": reg.description,
                    "default_value": reg.default_value,
                    "bits": [
                        {
                            "name": bit.name,
                            "position": bit.position,
                            "description": bit.description,
                            "default": bit.default
                        }
                        for bit in reg.bits
                    ]
                }
                for reg in self._registers.values()
            ]
        }
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
            
    def import_from_json(self, filepath: str):
        """Import register configuration from JSON file"""
        with open(filepath, 'r') as f:
            data = json.load(f)
            
        for reg_data in data.get("registers", []):
            bits = [
                BitDefinition(
                    bit["name"],
                    bit["position"],
                    bit.get("description", ""),
                    bit.get("default", 0)
                )
                for bit in reg_data.get("bits", [])
            ]
            
            register = RegisterDefinition(
                reg_data["name"],
                reg_data["address"],
                reg_data.get("description", ""),
                bits,
                reg_data.get("default_value", 0)
            )
            self.add_register(register)


class RegisterBuilder:
    """
    Fluent builder for creating register definitions.
    Provides a cleaner API for programmatic register creation.
    """
    
    def __init__(self):
        self._name = "REGISTER"
        self._address = 0x00
        self._description = ""
        self._bits: List[BitDefinition] = []
        self._default_value = 0
        
    def name(self, name: str) -> 'RegisterBuilder':
        """Set register name"""
        self._name = name
        return self
        
    def address(self, address: int) -> 'RegisterBuilder':
        """Set register address"""
        self._address = address
        return self
        
    def description(self, desc: str) -> 'RegisterBuilder':
        """Set register description"""
        self._description = desc
        return self
        
    def default_value(self, value: int) -> 'RegisterBuilder':
        """Set default value"""
        self._default_value = value
        return self
        
    def add_bit(self, name: str, position: int, description: str = "") -> 'RegisterBuilder':
        """Add a single bit definition"""
        self._bits.append(BitDefinition(name, position, description, (self._default_value >> position) & 1))
        return self
        
    def add_bits_from_names(self, names: List[str], descriptions: List[str] = None) -> 'RegisterBuilder':
        """Add multiple bits from name list (positions 0-9)"""
        for i, name in enumerate(names[:10]):
            desc = descriptions[i] if descriptions and i < len(descriptions) else ""
            self._bits.append(BitDefinition(name, i, desc, (self._default_value >> i) & 1))
        return self
        
    def build(self) -> RegisterDefinition:
        """Build the register definition"""
        # Ensure we have 10 bits
        while len(self._bits) < 10:
            pos = len(self._bits)
            self._bits.append(BitDefinition(f"BIT{pos}", pos, "", 0))
            
        # Sort by position
        self._bits.sort(key=lambda b: b.position)
        
        return RegisterDefinition(
            self._name,
            self._address,
            self._description,
            self._bits,
            self._default_value
        )


# ============================================================================
# Pre-defined additional registers (for expansion)
# ============================================================================

def get_additional_registers() -> List[RegisterDefinition]:
    """
    Get additional registers that can be added to the GD3160 map.
    These are example registers for demonstration purposes.
    """
    builder = RegisterBuilder
    
    return [
        # Example: STATUS register (read-only)
        builder()
            .name("STATUS1")
            .address(0x09)
            .description("Status Register 1 - Fault Flags")
            .add_bits_from_names(
                ["UV_FAULT", "OC_FAULT", "SC_FAULT", "DESAT_FAULT", "TEMP_WARN",
                 "TEMP_FAULT", "WDT_FAULT", "COM_FAULT", "BIST_FAIL", "RESERVED"],
                ["Under-voltage fault", "Over-current fault", "Short-circuit fault",
                 "Desaturation fault", "Temperature warning", "Temperature fault",
                 "Watchdog timeout", "Communication fault", "BIST failure", "Reserved"]
            )
            .build(),
            
        # Example: DIAG_CTRL register
        builder()
            .name("DIAG_CTRL")
            .address(0x0A)
            .description("Diagnostic Control Register")
            .add_bits_from_names(
                ["DIAG_EN", "DIAG_MODE[1]", "DIAG_MODE[0]", "DIAG_CHAN[3]", "DIAG_CHAN[2]",
                 "DIAG_CHAN[1]", "DIAG_CHAN[0]", "DIAG_RATE[1]", "DIAG_RATE[0]", "CONT_MODE"],
                ["Diagnostic enable", "Diagnostic mode bit 1", "Diagnostic mode bit 0",
                 "Diagnostic channel bit 3", "Diagnostic channel bit 2",
                 "Diagnostic channel bit 1", "Diagnostic channel bit 0",
                 "Diagnostic rate bit 1", "Diagnostic rate bit 0", "Continuous mode"]
            )
            .build(),
    ]


# ============================================================================
# Usage Examples
# ============================================================================

def example_usage():
    """Example usage of the customization helpers"""
    
    # Example 1: Using RegisterManager
    print("=== Example 1: RegisterManager ===")
    manager = RegisterManager()
    
    # Create a new register
    new_reg = manager.create_register(
        name="CUSTOM1",
        address=0x20,
        description="Custom Configuration Register",
        bit_names=["ENA", "ENB", "ENC", "MODE0", "MODE1", "CFG0", "CFG1", "CFG2", "TEST", "RST"],
        bit_descriptions=["Enable A", "Enable B", "Enable C", "Mode bit 0", "Mode bit 1",
                          "Config bit 0", "Config bit 1", "Config bit 2", "Test mode", "Reset"],
        default_value=0x00
    )
    print(f"Created register: {new_reg.name} at 0x{new_reg.address:02X}")
    
    # Modify a bit name
    manager.modify_bit_name("CUSTOM1", 0, "ENABLE_A")
    print(f"Modified bit 0 name to: {manager.get_register('CUSTOM1').bits[0].name}")
    
    # Example 2: Using RegisterBuilder
    print("\n=== Example 2: RegisterBuilder ===")
    custom_reg = (
        RegisterBuilder()
            .name("MY_CONFIG")
            .address(0x30)
            .description("My Custom Configuration")
            .default_value(0x15)
            .add_bit("POWER_EN", 0, "Power enable")
            .add_bit("DEBUG_MODE", 1, "Debug mode enable")
            .add_bit("SAFE_MODE", 2, "Safe mode flag")
            .add_bit("CLK_SEL", 3, "Clock selection")
            .add_bit("INT_EN", 4, "Interrupt enable")
            .build()
    )
    print(f"Built register: {custom_reg.name} with {len(custom_reg.bits)} bits")
    
    # Example 3: Export/Import
    print("\n=== Example 3: Export/Import ===")
    # manager.export_to_json("registers_config.json")
    # manager.import_from_json("registers_config.json")
    print("Export/Import methods available for JSON persistence")


if __name__ == "__main__":
    example_usage()
