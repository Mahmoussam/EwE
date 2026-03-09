"""
GD3160 Register Map Widget - Usage Examples
===========================================

This module demonstrates how to integrate the GD3160 Register Map Widget
into your PyQt5 applications.

Features:
- Light theme matching NXP FlexGUI
- Hex value boxes for write/read values
- Single callback pattern for Read/Write operations
- Reusable as QWidget or QTabWidget tab
"""

import sys
from typing import Dict, Optional
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QFrame, QStatusBar, QTabWidget, QSplitter,
    QGroupBox, QMessageBox
)

# Import GD3160 register models/list from device module
from E_Serial.GD3160.GD3160 import BitDefinition, RegisterDefinition, GD3160_REGISTERS

# Import the main widget components
from UIs.gd3160_register_widget import (
    RegisterMapWidget,
    RegisterViewWidget,
    FlexGUIColors
)


# ============================================================================
# Example 1: Basic Standalone Widget
# ============================================================================

def example_basic():
    """
    Example 1: Basic standalone usage.
    The simplest way to use the register map widget.
    """
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    window = QMainWindow()
    window.setWindowTitle("GD3160 Register Map - Basic Example")
    window.setGeometry(100, 100, 1000, 500)
    
    # Create widget without callbacks
    register_map = RegisterMapWidget()
    register_map.load_registers(GD3160_REGISTERS)
    
    window.setCentralWidget(register_map)
    window.show()
    
    sys.exit(app.exec_())


# ============================================================================
# Example 2: With Callbacks
# ============================================================================

class MainWindowWithCallbacks(QMainWindow):
    """
    Example 2: Main window with proper callback handling.
    Shows how to connect to hardware or simulation.
    """
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GD3160 Register Map - With Callbacks")
        self.setGeometry(100, 100, 1000, 500)
        
        # Simulated device state
        self._device_state: Dict[str, int] = {}
        for reg in GD3160_REGISTERS:
            self._device_state[reg.name] = reg.default_value
        
        self._setup_ui()
        
    def _setup_ui(self):
        """Setup the UI"""
        central = QWidget()
        layout = QVBoxLayout(central)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Create register map with callbacks
        self.register_map = RegisterMapWidget(
            on_write_callback=self._on_write,
            on_read_callback=self._on_read
        )
        self.register_map.load_registers(GD3160_REGISTERS)
        
        layout.addWidget(self.register_map)
        self.setCentralWidget(central)
        self.setStatusBar(QStatusBar())
        
    def _on_write(self, reg_view: RegisterViewWidget):
        """
        Write callback - receives the RegisterViewWidget.
        Access all register info and values from the widget.
        """
        name = reg_view.get_register_name()
        address = reg_view.get_register_address()
        value = reg_view.get_write_value()
        
        # Simulate hardware write
        self._device_state[name] = value
        
        # Update read value to reflect write
        reg_view.set_read_value(value)
        
        # Log the operation
        self.statusBar().showMessage(
            f"Write {name} (0x{address:02X}) = 0x{value:03X}", 3000
        )
        print(f"[HW Write] {name} @ 0x{address:02X} = 0x{value:03X}")
        
    def _on_read(self, reg_view: RegisterViewWidget):
        """
        Read callback - receives the RegisterViewWidget.
        Read from hardware and update the widget's read value.
        """
        name = reg_view.get_register_name()
        address = reg_view.get_register_address()
        
        # Simulate hardware read (in real app, do SPI/I2C read here)
        value = self._device_state.get(name, 0)
        
        # Update the widget's read display
        reg_view.set_read_value(value)
        
        # Log the operation
        self.statusBar().showMessage(
            f"Read {name} (0x{address:02X}) = 0x{value:03X}", 3000
        )
        print(f"[HW Read] {name} @ 0x{address:02X} = 0x{value:03X}")


def example_with_callbacks():
    """Run Example 2"""
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    window = MainWindowWithCallbacks()
    window.show()
    
    sys.exit(app.exec_())


# ============================================================================
# Example 3: As Tab in QTabWidget
# ============================================================================

class MultiTabWindow(QMainWindow):
    """
    Example 3: Using the register map as a tab in QTabWidget.
    Demonstrates integration into larger applications.
    """
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GD3160 Register Map - As Tab Widget")
        self.setGeometry(100, 100, 1100, 600)
        
        self._setup_ui()
        
    def _setup_ui(self):
        """Setup the UI with tabs"""
        central = QWidget()
        layout = QVBoxLayout(central)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Create tab widget
        tab_widget = QTabWidget()
        tab_widget.setStyleSheet(f"""
            QTabWidget::pane {{
                border: 1px solid {FlexGUIColors.BORDER_LIGHT};
                background: {FlexGUIColors.WINDOW_BG};
            }}
            QTabBar::tab {{
                background: #E0E0E0;
                padding: 8px 16px;
                border: 1px solid {FlexGUIColors.BORDER_LIGHT};
            }}
            QTabBar::tab:selected {{
                background: {FlexGUIColors.WINDOW_BG};
            }}
        """)
        
        # Tab 1: Register Map
        self.register_map = RegisterMapWidget(
            on_write_callback=self._on_write,
            on_read_callback=self._on_read
        )
        self.register_map.load_registers(GD3160_REGISTERS)
        tab_widget.addTab(self.register_map, "Register Map")
        
        # Tab 2: Placeholder for other functionality
        placeholder = QWidget()
        placeholder_layout = QVBoxLayout(placeholder)
        placeholder_layout.addWidget(QLabel("Other tabs can contain graphs, settings, etc."))
        tab_widget.addTab(placeholder, "Diagnostics")
        
        # Tab 3: Another placeholder
        placeholder2 = QWidget()
        placeholder2_layout = QVBoxLayout(placeholder2)
        placeholder2_layout.addWidget(QLabel("Configuration settings can go here."))
        tab_widget.addTab(placeholder2, "Settings")
        
        layout.addWidget(tab_widget)
        self.setCentralWidget(central)
        self.setStatusBar(QStatusBar())
        
    def _on_write(self, reg_view: RegisterViewWidget):
        """Write callback"""
        name = reg_view.get_register_name()
        value = reg_view.get_write_value()
        reg_view.set_read_value(value)
        self.statusBar().showMessage(f"Wrote {name} = 0x{value:03X}", 3000)
        
    def _on_read(self, reg_view: RegisterViewWidget):
        """Read callback"""
        import random
        name = reg_view.get_register_name()
        value = random.randint(0, 0x3FF)
        reg_view.set_read_value(value)
        self.statusBar().showMessage(f"Read {name} = 0x{value:03X}", 3000)


def example_as_tab():
    """Run Example 3"""
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    window = MultiTabWindow()
    window.show()
    
    sys.exit(app.exec_())


# ============================================================================
# Example 4: With Hardware Interface Class
# ============================================================================

class GD3160HardwareInterface:
    """
    Example hardware interface class.
    Replace the methods with actual SPI/I2C communication.
    """
    
    def __init__(self):
        # Simulated register storage
        self._registers: Dict[int, int] = {}
        for reg in GD3160_REGISTERS:
            self._registers[reg.address] = reg.default_value
            
    def write_register(self, address: int, value: int) -> bool:
        """
        Write to hardware register.
        Replace with actual SPI/I2C implementation.
        """
        # Example SPI write:
        # spi.write([address, (value >> 8) & 0x03, value & 0xFF])
        self._registers[address] = value & 0x3FF
        print(f"[SPI Write] Addr 0x{address:02X} = 0x{value:03X}")
        return True
        
    def read_register(self, address: int) -> int:
        """
        Read from hardware register.
        Replace with actual SPI/I2C implementation.
        """
        # Example SPI read:
        # response = spi.transfer([address | 0x80, 0, 0])
        # return (response[1] << 8) | response[2]
        value = self._registers.get(address, 0)
        print(f"[SPI Read] Addr 0x{address:02X} = 0x{value:03X}")
        return value
        
    def write_all(self, values: Dict[int, int]) -> bool:
        """Write multiple registers"""
        for addr, value in values.items():
            self.write_register(addr, value)
        return True
        
    def read_all(self) -> Dict[int, int]:
        """Read all registers"""
        return {addr: self.read_register(addr) for addr in self._registers}


class HardwareIntegratedWindow(QMainWindow):
    """
    Example 4: Full hardware integration.
    Uses the hardware interface for read/write operations.
    """
    
    def __init__(self, hardware: GD3160HardwareInterface):
        super().__init__()
        self._hw = hardware
        self._address_map = {reg.name: reg.address for reg in GD3160_REGISTERS}
        
        self.setWindowTitle("GD3160 Register Map - Hardware Integration")
        self.setGeometry(100, 100, 1000, 500)
        
        self._setup_ui()
        
    def _setup_ui(self):
        """Setup UI"""
        central = QWidget()
        layout = QVBoxLayout(central)
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.register_map = RegisterMapWidget(
            on_write_callback=self._hw_write,
            on_read_callback=self._hw_read
        )
        self.register_map.load_registers(GD3160_REGISTERS)
        
        layout.addWidget(self.register_map)
        self.setCentralWidget(central)
        self.setStatusBar(QStatusBar())
        
    def _hw_write(self, reg_view: RegisterViewWidget):
        """Write to hardware"""
        name = reg_view.get_register_name()
        address = self._address_map[name]
        value = reg_view.get_write_value()
        
        # Write to hardware
        success = self._hw.write_register(address, value)
        
        if success:
            # Read back to confirm
            read_value = self._hw.read_register(address)
            reg_view.set_read_value(read_value)
            self.statusBar().showMessage(
                f"Wrote {name} = 0x{value:03X}, Read back = 0x{read_value:03X}", 3000
            )
        else:
            self.statusBar().showMessage(f"Write failed for {name}", 3000)
            
    def _hw_read(self, reg_view: RegisterViewWidget):
        """Read from hardware"""
        name = reg_view.get_register_name()
        address = self._address_map[name]
        
        # Read from hardware
        value = self._hw.read_register(address)
        reg_view.set_read_value(value)
        
        self.statusBar().showMessage(f"Read {name} = 0x{value:03X}", 3000)


def example_hardware_integration():
    """Run Example 4"""
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    hardware = GD3160HardwareInterface()
    window = HardwareIntegratedWindow(hardware)
    window.show()
    
    sys.exit(app.exec_())


# ============================================================================
# Example 5: Dynamic Register Management
# ============================================================================

class DynamicManagementWindow(QMainWindow):
    """
    Example 5: Adding/removing registers at runtime.
    Useful for custom configurations.
    """
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GD3160 Register Map - Dynamic Management")
        self.setGeometry(100, 100, 1000, 550)
        
        self._setup_ui()
        
    def _setup_ui(self):
        """Setup UI with control panel"""
        central = QWidget()
        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Control panel
        control_panel = self._create_control_panel()
        main_layout.addWidget(control_panel)
        
        # Register map
        self.register_map = RegisterMapWidget(
            on_write_callback=self._on_write,
            on_read_callback=self._on_read
        )
        self.register_map.load_registers(GD3160_REGISTERS)
        main_layout.addWidget(self.register_map)
        
        self.setCentralWidget(central)
        self.setStatusBar(QStatusBar())
        
    def _create_control_panel(self) -> QFrame:
        """Create control panel"""
        panel = QFrame()
        panel.setStyleSheet(f"""
            QFrame {{
                background-color: #E8E8E8;
                border-bottom: 1px solid {FlexGUIColors.BORDER_LIGHT};
            }}
        """)
        panel.setFixedHeight(50)
        
        layout = QHBoxLayout(panel)
        layout.setContentsMargins(10, 5, 10, 5)
        
        # Add custom register button
        btn_add = QPushButton("Add Custom Register")
        btn_add.setStyleSheet(f"""
            QPushButton {{
                background-color: #2196F3;
                color: white;
                border: none;
                border-radius: 3px;
                padding: 6px 12px;
            }}
            QPushButton:hover {{ background-color: #1976D2; }}
        """)
        btn_add.clicked.connect(self._add_custom_register)
        layout.addWidget(btn_add)
        
        # Reset to defaults button
        btn_reset = QPushButton("Reset Defaults")
        btn_reset.setStyleSheet(f"""
            QPushButton {{
                background-color: #FF9800;
                color: white;
                border: none;
                border-radius: 3px;
                padding: 6px 12px;
            }}
            QPushButton:hover {{ background-color: #F57C00; }}
        """)
        btn_reset.clicked.connect(self._reset_defaults)
        layout.addWidget(btn_reset)
        
        layout.addStretch()
        
        return panel
        
    def _add_custom_register(self):
        """Add a custom register"""
        custom_reg = RegisterDefinition(
            name="CUSTOM",
            address=0x20,
            description="Custom Register",
            bits=[
                BitDefinition(f"BIT{i}", i, f"Custom bit {i}", 0)
                for i in range(10)
            ],
            default_value=0
        )
        self.register_map.add_register(custom_reg)
        self.statusBar().showMessage("Added CUSTOM register", 3000)
        
    def _reset_defaults(self):
        """Reset to default registers"""
        self.register_map.load_registers(GD3160_REGISTERS)
        self.statusBar().showMessage("Reset to default registers", 3000)
        
    def _on_write(self, reg_view: RegisterViewWidget):
        reg_view.set_read_value(reg_view.get_write_value())
        self.statusBar().showMessage(f"Wrote {reg_view.get_register_name()}", 3000)
        
    def _on_read(self, reg_view: RegisterViewWidget):
        import random
        reg_view.set_read_value(random.randint(0, 0x3FF))
        self.statusBar().showMessage(f"Read {reg_view.get_register_name()}", 3000)


def example_dynamic():
    """Run Example 5"""
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    window = DynamicManagementWindow()
    window.show()
    
    sys.exit(app.exec_())


# ============================================================================
# Main Entry Point
# ============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("GD3160 Register Map Widget - Usage Examples")
    print("=" * 60)
    print("\nAvailable examples:")
    print("  1. example_basic()            - Basic standalone widget")
    print("  2. example_with_callbacks()   - With read/write callbacks")
    print("  3. example_as_tab()           - As tab in QTabWidget")
    print("  4. example_hardware_integration() - Hardware interface")
    print("  5. example_dynamic()          - Dynamic register management")
    print("\nRunning Example 2 (With Callbacks)...")
    print("-" * 60)
    
    # Run the default example
    example_with_callbacks()
