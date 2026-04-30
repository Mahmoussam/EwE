from PyQt5 import QtWidgets, uic
from PyQt5.QtGui import QPixmap
from E_Serial import ReadMessage
from E_Serial.GD3160.GD3160 import GD3160_REGISTERS
from UIs.gd3160_register_widget import RegisterMapWidget, RegisterViewWidget
from UIs.gate_drive_window import GateDriveWindow
from UIs.current_sense_window import CurrentSenseWindow
import os
import asyncio
from datetime import datetime

# Import background images resources  
try:
    from . import background_images_rc
except ImportError:
    import background_images_rc


class GDControlPanel(QtWidgets.QWidget):
    def __init__(self, serial_dispatcher, daisyChainIndex=0):
        """
        Initialize the GD3160 Control Panel
        
        Args:
            serial_dispatcher: Reference to the SerialDispatcher instance for async messaging
            daisyChainIndex: Zero-based index of the GD in the daisy chain
        """
        super().__init__()
        self.__dispatcher = serial_dispatcher
        self.daisyChainIndex = daisyChainIndex
        
        # Load the UI with absolute path
        ui_path = os.path.join(os.path.dirname(__file__), "gd_control_panel.ui")
        uic.loadUi(ui_path, self)
        
        # Set window properties
        self.setWindowTitle(f"GD3160 Control Panel [DX={self.daisyChainIndex}]")
        
        # Setup register map tab
        self._setup_register_map_tab()
        
        # Setup gate drive tab
        self._setup_gate_drive_tab()
        
        # Setup current sense tab
        self._setup_current_sense_tab()
        
        # TODO: Connect button signals and setup UI interactions
        # Example:
        # self.some_button.clicked.connect(
        #     lambda: asyncio.create_task(self.__on_some_button_clicked())
        # )
    
    def _setup_register_map_tab(self):
        """Setup the register map tab with callbacks"""
        # Create register map widget with callbacks
        self.register_map = RegisterMapWidget(
            on_write_callback=self._on_register_write,
            on_read_callback=self._on_register_read
        )
        
        # Load GD3160 registers
        self.register_map.load_registers(GD3160_REGISTERS)
        
        # Add to the first tab (index 0) of control_panel_tab_widget
        # Clear the tab first if it has placeholder content
        if self.control_panel_tab_widget.count() > 0:
            # Remove existing tab at index 0 if present
            self.control_panel_tab_widget.removeTab(0)
        
        # Add the register map as the first tab
        self.control_panel_tab_widget.insertTab(0, self.register_map, "Register Map")
    
    def _setup_gate_drive_tab(self):
        """Setup the gate drive tab"""
        # Create gate drive window widget
        self.gate_drive = GateDriveWindow()
        
        # Add as a tab to control_panel_tab_widget
        self.control_panel_tab_widget.addTab(self.gate_drive, "Gate Drive")
    
    def _setup_current_sense_tab(self):
        """Setup the current sense tab"""
        # Create current sense window widget
        self.current_sense = CurrentSenseWindow()
        
        # Add as a tab to control_panel_tab_widget
        self.control_panel_tab_widget.addTab(self.current_sense, "Current Sense")
        
    def _on_register_write(self, reg_view: RegisterViewWidget):
        """
        Write callback for register map - sends write command via serial dispatcher.
        
        Args:
            reg_view: RegisterViewWidget containing register info and write value
        """
        name = reg_view.get_register_name()
        address = reg_view.get_register_address()
        value = reg_view.get_write_value()
        
        print(f"[GDControlPanel][DX={self.daisyChainIndex}] Write request: {name} (0x{address:02X}) = 0x{value:03X}")
        
        if self.__dispatcher is None:
            print(f"[GDControlPanel][DX={self.daisyChainIndex}] ERROR: Serial dispatcher not available")
            # Still update the read value for UI feedback in test mode
            # reg_view.set_read_value(value)
            return
        
        # Create async task to write register
        asyncio.create_task(self._async_write_register(reg_view, address, value))
        
    async def _async_write_register(self, reg_view: RegisterViewWidget, address: int, value: int):
        """Async handler for register write"""
        try:
            response = await self.__dispatcher.write_register(address, value, timeout=2.0, dx=self.daisyChainIndex)
            print(f"[GDControlPanel][DX={self.daisyChainIndex}] Write successful: {response}")
            # Update read value to reflect write
            reg_view.set_read_value(value)
        except asyncio.TimeoutError:
            print(f"[GDControlPanel][DX={self.daisyChainIndex}] Write timeout for addr 0x{address:02X}")
        except Exception as ex:
            print(f"[GDControlPanel][DX={self.daisyChainIndex}] Write error: {ex}")
    
    def _on_register_read(self, reg_view: RegisterViewWidget):
        """
        Read callback for register map - sends read command via serial dispatcher.
        
        Args:
            reg_view: RegisterViewWidget containing register info
        """
        name = reg_view.get_register_name()
        address = reg_view.get_register_address()
        
        print(f"[GDControlPanel][DX={self.daisyChainIndex}] Read request: {name} (0x{address:02X})")
        
        if self.__dispatcher is None:
            print(f"[GDControlPanel][DX={self.daisyChainIndex}] ERROR: Serial dispatcher not available")
            # Set dummy value for test mode
            reg_view.set_read_value(0x000)
            return
        
        # Create async task to read register
        asyncio.create_task(self._async_read_register(reg_view, address))
        
    async def _async_read_register(self, reg_view: RegisterViewWidget, address: int):
        """Async handler for register read"""
        try:
            data = await self.__dispatcher.read_register(address, timeout=2.0, dx=self.daisyChainIndex)
            print(f"[GDControlPanel][DX={self.daisyChainIndex}] Read successful: 0x{data:03X}")
            # Update the widget's read display
            reg_view.set_read_value(data)
        except asyncio.TimeoutError:
            print(f"[GDControlPanel][DX={self.daisyChainIndex}] Read timeout for addr 0x{address:02X}")
        except Exception as ex:
            print(f"[GDControlPanel][DX={self.daisyChainIndex}] Read error: {ex}")


if __name__ == '__main__':
    import sys
    from qasync import QEventLoop
    
    # Create the QApplication
    app = QtWidgets.QApplication(sys.argv)
    
    # Set up asyncio event loop for qasync
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)
    
    # Create the control panel with None dispatcher for testing
    window = GDControlPanel(None)
    window.show()
    
    # Run the application with asyncio support
    with loop:
        loop.run_forever()
        
