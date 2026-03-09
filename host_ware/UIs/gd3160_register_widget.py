"""
GD3160 Register Map Widget for PyQt5
A FlexGUI-style register mapping interface for NXP GD3160 Gate Driver

Features:
- Light theme matching NXP FlexGUI colors
- Hex value boxes next to W/R buttons
- CONFIGAOUT register included
- Single callback pattern for Read/Write operations
- Reusable as QWidget or QTabWidget tab

Author: Super Z
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, 
    QScrollArea, QFrame, QSizePolicy, QLineEdit, QSpacerItem,
    QApplication, QMainWindow, QTabWidget
)
from PyQt5.QtCore import Qt, pyqtSignal, QTimer
from PyQt5.QtGui import QFont, QCursor, QColor, QPalette, QDoubleValidator
from typing import Dict, List, Optional, Tuple, Callable
from E_Serial.GD3160.GD3160 import BitDefinition, RegisterDefinition, GD3160_REGISTERS


# ============================================================================
# FlexGUI Color Scheme (Light Theme)
# ============================================================================

class FlexGUIColors:
    """Color scheme matching NXP FlexGUI"""
    # Background colors
    WINDOW_BG = "#F0F0F0"           # Main window background
    PANEL_BG = "#FFFFFF"            # Panel/register background
    PANEL_BG_ALT = "#F8F8F8"        # Alternate row background
    
    # Bit button colors
    BIT_0_BG = "#FF9999"            # Light red/coral for bit = 0
    BIT_1_BG = "#99FF99"            # Light green for bit = 1
    BIT_0_HOVER = "#FF7777"         # Darker red on hover
    BIT_1_HOVER = "#77DD77"         # Darker green on hover
    
    # Text colors
    TEXT_PRIMARY = "#333333"        # Primary text (dark gray)
    TEXT_SECONDARY = "#666666"      # Secondary text
    TEXT_VALUE = "#000000"          # Value text (black)
    TEXT_LIGHT = "#FFFFFF"          # Light text on dark backgrounds
    
    # Button colors
    BUTTON_BG = "#FFFFFF"           # Button background
    BUTTON_BORDER = "#AAAAAA"       # Button border
    BUTTON_HOVER = "#E8E8E8"        # Button hover
    WRITE_BTN_BG = "#4CAF50"        # Write button green
    WRITE_BTN_HOVER = "#45a049"     # Write button hover
    READ_BTN_BG = "#2196F3"         # Read button blue
    READ_BTN_HOVER = "#1976D2"      # Read button hover
    
    # Hex box colors
    HEX_BOX_BG = "#FFFFFF"          # Hex value box background
    HEX_BOX_BORDER = "#CCCCCC"      # Hex value box border
    HEX_BOX_READONLY_BG = "#F5F5F5" # Read-only hex box background
    
    # Border colors
    BORDER_LIGHT = "#DDDDDD"        # Light border
    BORDER_MEDIUM = "#AAAAAA"       # Medium border
    BORDER_DARK = "#666666"         # Dark border


# ============================================================================
# Hex Value Box Widget
# ============================================================================

class HexValueBox(QLineEdit):
    """Hex value input/display box"""
    
    valueChanged = pyqtSignal(int)  # Emits new integer value
    
    def __init__(self, is_read_only: bool = False, parent=None):
        super().__init__(parent)
        self._is_read_only = is_read_only
        self._value = 0
        self._setup_ui()
        
    def _setup_ui(self):
        """Setup the hex box UI"""
        self.setFixedSize(55, 24)
        self.setFont(QFont("Consolas", 9, QFont.Bold))
        self.setAlignment(Qt.AlignCenter)
        self.setReadOnly(self._is_read_only)
        
        if self._is_read_only:
            self.setStyleSheet(f"""
                QLineEdit {{
                    background-color: {FlexGUIColors.HEX_BOX_READONLY_BG};
                    color: {FlexGUIColors.TEXT_VALUE};
                    border: 1px solid {FlexGUIColors.HEX_BOX_BORDER};
                    border-radius: 3px;
                    padding: 2px;
                }}
            """)
        else:
            self.setStyleSheet(f"""
                QLineEdit {{
                    background-color: {FlexGUIColors.HEX_BOX_BG};
                    color: {FlexGUIColors.TEXT_VALUE};
                    border: 1px solid {FlexGUIColors.HEX_BOX_BORDER};
                    border-radius: 3px;
                    padding: 2px;
                }}
                QLineEdit:focus {{
                    border: 2px solid {FlexGUIColors.READ_BTN_BG};
                }}
            """)
        self._update_display()
        
    def _update_display(self):
        """Update the display with current value"""
        self.setText(f"0x{self._value:03X}")
        
    def set_value(self, value: int):
        """Set the value (clamped to 10-bit)"""
        self._value = value & 0x3FF  # 10-bit mask
        self._update_display()
        
    def get_value(self) -> int:
        """Get the current value"""
        return self._value
        
    def keyPressEvent(self, event):
        """Handle key press for hex input"""
        if self._is_read_only:
            return
            
        key = event.text().upper()
        
        # Allow hex digits
        if key in '0123456789ABCDEF':
            current = self.text().replace('0x', '')
            if len(current) < 3:
                new_text = current + key
                try:
                    self._value = int(new_text, 16) & 0x3FF
                    self._update_display()
                    self.valueChanged.emit(self._value)
                except ValueError:
                    pass
        elif event.key() == Qt.Key_Backspace:
            current = self.text().replace('0x', '')
            if len(current) > 0:
                new_text = current[:-1]
                try:
                    self._value = int(new_text, 16) if new_text else 0
                    self._update_display()
                    self.valueChanged.emit(self._value)
                except ValueError:
                    self._value = 0
                    self._update_display()
        else:
            super().keyPressEvent(event)
            
    def focusOutEvent(self, event):
        """Handle focus out - reset to valid display"""
        self._update_display()
        super().focusOutEvent(event)


# ============================================================================
# Bit Button Widget (FlexGUI Style)
# ============================================================================

class BitButton(QPushButton):
    """
    A clickable button representing a single bit in a register.
    FlexGUI Light Theme:
    - Light red/coral background = bit is 0
    - Light green background = bit is 1
    """
    
    bitClicked = pyqtSignal(int, int)  # (bit_position, new_value)
    
    def __init__(self, bit_definition: BitDefinition, parent=None):
        super().__init__(parent)
        self.bit_def = bit_definition
        self._value = bit_definition.default
        self._is_read_only = False
        self._is_hovering = False
        
        self._setup_ui()
        self._update_style()
        
    def _setup_ui(self):
        """Initialize the button UI"""
        self.setText(self.bit_def.name)
        self.setFixedSize(80, 26)
        self.setFont(QFont("Segoe UI", 7, QFont.Bold))
        self.setCursor(QCursor(Qt.PointingHandCursor))
        self.setToolTip(f"{self.bit_def.name}\n{self.bit_def.description}\nPosition: Bit {self.bit_def.position}")
        
    def _update_style(self):
        """Update the button stylesheet based on current value"""
        if self._value == 1:
            bg_color = FlexGUIColors.BIT_1_HOVER if self._is_hovering else FlexGUIColors.BIT_1_BG
        else:
            bg_color = FlexGUIColors.BIT_0_HOVER if self._is_hovering else FlexGUIColors.BIT_0_BG
            
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {bg_color};
                color: {FlexGUIColors.TEXT_PRIMARY};
                border: 1px solid {FlexGUIColors.BORDER_MEDIUM};
                border-radius: 3px;
                padding: 2px 3px;
                text-align: center;
            }}
            QPushButton:pressed {{
                background-color: #CCCCCC;
            }}
            QPushButton:disabled {{
                background-color: #DDDDDD;
                color: #999999;
            }}
        """)
        
    def enterEvent(self, event):
        """Handle mouse enter for hover effect"""
        self._is_hovering = True
        self._update_style()
        super().enterEvent(event)
        
    def leaveEvent(self, event):
        """Handle mouse leave for hover effect"""
        self._is_hovering = False
        self._update_style()
        super().leaveEvent(event)
        
    def mousePressEvent(self, event):
        """Handle click to toggle bit value"""
        if self._is_read_only:
            return
            
        if event.button() == Qt.LeftButton:
            # Toggle the bit
            self._value = 0 if self._value == 1 else 1
            self._update_style()
            self.bitClicked.emit(self.bit_def.position, self._value)
            
        super().mousePressEvent(event)
        
    def set_value(self, value: int):
        """Set the bit value (0 or 1)"""
        if value in (0, 1) and self._value != value:
            self._value = value
            self._update_style()
            
    def get_value(self) -> int:
        """Get the current bit value"""
        return self._value
        
    def set_read_only(self, read_only: bool):
        """Set whether the bit is read-only"""
        self._is_read_only = read_only
        self.setEnabled(not read_only)
        self.setCursor(QCursor(Qt.ForbiddenCursor) if read_only else Qt.PointingHandCursor)


# ============================================================================
# Read Bit Display Widget
# ============================================================================

class ReadBitDisplay(QLabel):
    """Display-only widget showing the read value of a bit"""
    
    def __init__(self, bit_definition: BitDefinition, parent=None):
        super().__init__(parent)
        self.bit_def = bit_definition
        self._value = 0
        
        self._setup_ui()
        self._update_style()
        
    def _setup_ui(self):
        """Initialize the display UI"""
        self.setText(self.bit_def.name)
        self.setFixedSize(80, 26)
        self.setFont(QFont("Segoe UI", 7, QFont.Bold))
        self.setAlignment(Qt.AlignCenter)
        self.setToolTip(f"READ: {self.bit_def.name}\n{self.bit_def.description}")
        
    def _update_style(self):
        """Update the display stylesheet based on current value"""
        bg_color = FlexGUIColors.BIT_1_BG if self._value == 1 else FlexGUIColors.BIT_0_BG
        self.setStyleSheet(f"""
            QLabel {{
                background-color: {bg_color};
                color: {FlexGUIColors.TEXT_PRIMARY};
                border: 1px solid {FlexGUIColors.BORDER_MEDIUM};
                border-radius: 3px;
                padding: 2px 3px;
            }}
        """)
        
    def set_value(self, value: int):
        """Set the displayed bit value"""
        if value in (0, 1) and self._value != value:
            self._value = value
            self._update_style()
            
    def get_value(self) -> int:
        """Get the current displayed value"""
        return self._value


# ============================================================================
# Register View Widget
# ============================================================================

class RegisterViewWidget(QFrame):
    """
    A widget displaying a single register with:
    - Register name and address
    - Write/Read buttons with hex value boxes
    - Write bit buttons (row 1) - interactive
    - Read bit displays (row 2) - display only
    
    Callbacks:
    - on_write_callback(register_view): Called when Write button clicked
    - on_read_callback(register_view): Called when Read button clicked
    """
    
    def __init__(
        self, 
        register_def: RegisterDefinition,
        on_write_callback: Callable[['RegisterViewWidget'], None] = None,
        on_read_callback: Callable[['RegisterViewWidget'], None] = None,
        parent=None
    ):
        super().__init__(parent)
        self.register_def = register_def
        self._on_write_callback = on_write_callback
        self._on_read_callback = on_read_callback
        
        self._write_value = register_def.default_value
        self._read_value = 0
        self._write_bits: Dict[int, BitButton] = {}
        self._read_bits: Dict[int, ReadBitDisplay] = {}
        
        self._setup_ui()
        self._connect_signals()
        
        # Initialize with default value
        self.set_write_value(register_def.default_value)
        
    def _setup_ui(self):
        """Initialize the register widget UI"""
        # Alternate background for rows
        bg_color = FlexGUIColors.PANEL_BG if self.register_def.address % 2 == 0 else FlexGUIColors.PANEL_BG_ALT
        
        self.setFrameStyle(QFrame.StyledPanel | QFrame.Raised)
        self.setStyleSheet(f"""
            RegisterViewWidget {{
                background-color: {bg_color};
                border: 1px solid {FlexGUIColors.BORDER_LIGHT};
                border-radius: 4px;
                margin: 1px;
            }}
        """)
        
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(6, 4, 6, 4)
        main_layout.setSpacing(6)
        
        # Left panel: Register name and address
        left_panel = self._create_left_panel()
        main_layout.addLayout(left_panel)
        
        # Middle panel: Control buttons and hex boxes
        middle_panel = self._create_control_panel()
        main_layout.addLayout(middle_panel)
        
        # Right panel: Bit fields
        right_panel = self._create_bit_panel()
        main_layout.addLayout(right_panel, 1)
        
    def _create_left_panel(self) -> QVBoxLayout:
        """Create the left panel with register name and address"""
        layout = QVBoxLayout()
        layout.setSpacing(1)
        
        # Register name
        name_label = QLabel(self.register_def.name)
        name_label.setFont(QFont("Segoe UI", 9, QFont.Bold))
        name_label.setStyleSheet(f"color: {FlexGUIColors.TEXT_PRIMARY}; background: transparent;")
        name_label.setFixedWidth(75)
        layout.addWidget(name_label)
        
        # Address
        addr_label = QLabel(f"0x{self.register_def.address:02X}")
        addr_label.setFont(QFont("Consolas", 8))
        addr_label.setStyleSheet(f"color: {FlexGUIColors.TEXT_SECONDARY}; background: transparent;")
        addr_label.setFixedWidth(75)
        layout.addWidget(addr_label)
        
        return layout
        
    def _create_control_panel(self) -> QVBoxLayout:
        """Create the Write/Read buttons with hex value boxes"""
        layout = QVBoxLayout()
        layout.setSpacing(3)
        
        # Write row: Button + Hex box
        write_row = QHBoxLayout()
        write_row.setSpacing(3)
        
        self.btn_write = QPushButton("W")
        self.btn_write.setFixedSize(28, 22)
        self.btn_write.setFont(QFont("Segoe UI", 8, QFont.Bold))
        self.btn_write.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_write.setToolTip(f"Write {self.register_def.name} to device")
        self.btn_write.setStyleSheet(f"""
            QPushButton {{
                background-color: {FlexGUIColors.WRITE_BTN_BG};
                color: {FlexGUIColors.TEXT_LIGHT};
                border: 1px solid #3d8b40;
                border-radius: 3px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {FlexGUIColors.WRITE_BTN_HOVER};
            }}
            QPushButton:pressed {{
                background-color: #3d8b40;
            }}
        """)
        write_row.addWidget(self.btn_write)
        
        self.hex_write = HexValueBox(is_read_only=False)
        self.hex_write.setToolTip(f"Write value for {self.register_def.name}")
        write_row.addWidget(self.hex_write)
        
        layout.addLayout(write_row)
        
        # Read row: Button + Hex box (read-only)
        read_row = QHBoxLayout()
        read_row.setSpacing(3)
        
        self.btn_read = QPushButton("R")
        self.btn_read.setFixedSize(28, 22)
        self.btn_read.setFont(QFont("Segoe UI", 8, QFont.Bold))
        self.btn_read.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_read.setToolTip(f"Read {self.register_def.name} from device")
        self.btn_read.setStyleSheet(f"""
            QPushButton {{
                background-color: {FlexGUIColors.READ_BTN_BG};
                color: {FlexGUIColors.TEXT_LIGHT};
                border: 1px solid #1976D2;
                border-radius: 3px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {FlexGUIColors.READ_BTN_HOVER};
            }}
            QPushButton:pressed {{
                background-color: #1565C0;
            }}
        """)
        read_row.addWidget(self.btn_read)
        
        self.hex_read = HexValueBox(is_read_only=True)
        self.hex_read.setToolTip(f"Read value from {self.register_def.name}")
        read_row.addWidget(self.hex_read)
        
        layout.addLayout(read_row)
        
        return layout
        
    def _create_bit_panel(self) -> QVBoxLayout:
        """Create the bit fields panel with write and read rows"""
        layout = QVBoxLayout()
        layout.setSpacing(2)
        
        # Row labels
        label_layout = QHBoxLayout()
        label_layout.setSpacing(2)
        
        write_label = QLabel("W:")
        write_label.setFont(QFont("Segoe UI", 7))
        write_label.setStyleSheet(f"color: {FlexGUIColors.TEXT_SECONDARY}; background: transparent;")
        write_label.setFixedWidth(18)
        label_layout.addWidget(write_label)
        
        # Write bits row
        write_layout = QHBoxLayout()
        write_layout.setSpacing(2)
        write_layout.addWidget(write_label)
        
        for bit_def in self.register_def.bits:
            bit_btn = BitButton(bit_def)
            self._write_bits[bit_def.position] = bit_btn
            write_layout.addWidget(bit_btn)
            
        write_layout.addStretch()
        layout.addLayout(write_layout)
        
        # Read bits row
        read_layout = QHBoxLayout()
        read_layout.setSpacing(2)
        
        read_label = QLabel("R:")
        read_label.setFont(QFont("Segoe UI", 7))
        read_label.setStyleSheet(f"color: {FlexGUIColors.TEXT_SECONDARY}; background: transparent;")
        read_label.setFixedWidth(18)
        read_layout.addWidget(read_label)
        
        for bit_def in self.register_def.bits:
            read_display = ReadBitDisplay(bit_def)
            self._read_bits[bit_def.position] = read_display
            read_layout.addWidget(read_display)
            
        read_layout.addStretch()
        layout.addLayout(read_layout)
        
        return layout
        
    def _connect_signals(self):
        """Connect internal signals"""
        self.btn_write.clicked.connect(self._on_write_clicked)
        self.btn_read.clicked.connect(self._on_read_clicked)
        
        # Connect bit buttons to update hex value
        for pos, bit_btn in self._write_bits.items():
            bit_btn.bitClicked.connect(self._on_bit_changed)
            
        # Connect hex box value change
        self.hex_write.valueChanged.connect(self._on_hex_changed)
        
    def _on_write_clicked(self):
        """Handle write button click - calls the callback with self"""
        if self._on_write_callback:
            self._on_write_callback(self)
            
    def _on_read_clicked(self):
        """Handle read button click - calls the callback with self"""
        if self._on_read_callback:
            self._on_read_callback(self)
            
    def _on_bit_changed(self, position: int, value: int):
        """Handle bit value change - update hex display"""
        self._update_write_value()
        
    def _on_hex_changed(self, value: int):
        """Handle hex box value change - update bits"""
        self.set_write_value(value)
        
    def _update_write_value(self):
        """Update hex display from bits"""
        value = self.get_write_value()
        self._write_value = value
        self.hex_write.blockSignals(True)
        self.hex_write.set_value(value)
        self.hex_write.blockSignals(False)
        
    def get_write_value(self) -> int:
        """Get the current write value from all write bits"""
        value = 0
        for pos, bit_btn in self._write_bits.items():
            if bit_btn.get_value():
                value |= (1 << pos)
        return value
        
    def set_write_value(self, value: int):
        """Set the write bit values"""
        self._write_value = value & 0x3FF  # 10-bit mask
        
        for pos, bit_btn in self._write_bits.items():
            bit_val = (self._write_value >> pos) & 1
            bit_btn.blockSignals(True)
            bit_btn.set_value(bit_val)
            bit_btn.blockSignals(False)
            
        self.hex_write.blockSignals(True)
        self.hex_write.set_value(self._write_value)
        self.hex_write.blockSignals(False)
            
    def set_read_value(self, value: int):
        """Set the read bit display values"""
        self._read_value = value & 0x3FF  # 10-bit mask
        
        for pos, read_display in self._read_bits.items():
            bit_val = (self._read_value >> pos) & 1
            read_display.set_value(bit_val)
            
        self.hex_read.set_value(self._read_value)
            
    def get_read_value(self) -> int:
        """Get the current read value"""
        return self._read_value
        
    def get_register_name(self) -> str:
        """Get the register name"""
        return self.register_def.name
        
    def get_register_address(self) -> int:
        """Get the register address"""
        return self.register_def.address
        
    def set_callbacks(
        self,
        on_write: Callable[['RegisterViewWidget'], None] = None,
        on_read: Callable[['RegisterViewWidget'], None] = None
    ):
        """Set or update the callbacks"""
        if on_write:
            self._on_write_callback = on_write
        if on_read:
            self._on_read_callback = on_read
            
    def set_write_enabled(self, enabled: bool):
        """Enable/disable write functionality"""
        self.btn_write.setEnabled(enabled)
        self.hex_write.setEnabled(enabled)
        for bit_btn in self._write_bits.values():
            bit_btn.setEnabled(enabled)
        
    def set_read_enabled(self, enabled: bool):
        """Enable/disable read functionality"""
        self.btn_read.setEnabled(enabled)


# ============================================================================
# Register Map Widget (Main Container)
# ============================================================================

class RegisterMapWidget(QWidget):
    """
    Main widget containing a scrollable list of RegisterViewWidget items.
    Can be used as a standalone widget or added to a QTabWidget.
    
    Usage:
        widget = RegisterMapWidget()
        widget.set_callbacks(on_write=my_write_handler, on_read=my_read_handler)
        widget.load_registers(GD3160_REGISTERS)
    """
    
    def __init__(
        self,
        on_write_callback: Callable[[RegisterViewWidget], None] = None,
        on_read_callback: Callable[[RegisterViewWidget], None] = None,
        parent=None
    ):
        super().__init__(parent)
        self._register_widgets: Dict[str, RegisterViewWidget] = {}
        self._on_write_callback = on_write_callback
        self._on_read_callback = on_read_callback
        
        self._setup_ui()
        
    def _setup_ui(self):
        """Initialize the main widget UI"""
        self.setStyleSheet(f"background-color: {FlexGUIColors.WINDOW_BG};")
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Header with controls
        header = self._create_header()
        main_layout.addWidget(header)
        
        # Scrollable register list
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scroll_area.setStyleSheet(f"""
            QScrollArea {{
                border: none;
                background-color: {FlexGUIColors.WINDOW_BG};
            }}
            QScrollBar:vertical {{
                border: none;
                background: {FlexGUIColors.PANEL_BG_ALT};
                width: 14px;
                margin: 0;
            }}
            QScrollBar::handle:vertical {{
                background: #CCCCCC;
                border-radius: 7px;
                min-height: 30px;
            }}
            QScrollBar::handle:vertical:hover {{
                background: #BBBBBB;
            }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                height: 0;
            }}
        """)
        
        # Container for register widgets
        self.register_container = QWidget()
        self.register_container.setStyleSheet(f"background-color: {FlexGUIColors.WINDOW_BG};")
        self.register_layout = QVBoxLayout(self.register_container)
        self.register_layout.setContentsMargins(4, 4, 4, 4)
        self.register_layout.setSpacing(4)
        self.register_layout.addStretch()
        
        self.scroll_area.setWidget(self.register_container)
        main_layout.addWidget(self.scroll_area, 1)
        
    def _create_header(self) -> QFrame:
        """Create the header with global controls"""
        header = QFrame()
        header.setStyleSheet(f"""
            QFrame {{
                background-color: #E0E0E0;
                border: none;
                border-bottom: 1px solid {FlexGUIColors.BORDER_LIGHT};
            }}
        """)
        header.setFixedHeight(40)
        
        layout = QHBoxLayout(header)
        layout.setContentsMargins(10, 5, 10, 5)
        
        # Title
        title = QLabel("GD3160 Register Map")
        title.setFont(QFont("Segoe UI", 10, QFont.Bold))
        title.setStyleSheet(f"color: {FlexGUIColors.TEXT_PRIMARY}; background: transparent;")
        layout.addWidget(title)
        
        layout.addStretch()
        
        # Read All button
        self.btn_read_all = QPushButton("Read All")
        self.btn_read_all.setFixedSize(75, 26)
        self.btn_read_all.setFont(QFont("Segoe UI", 8))
        self.btn_read_all.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_read_all.setStyleSheet(f"""
            QPushButton {{
                background-color: {FlexGUIColors.READ_BTN_BG};
                color: {FlexGUIColors.TEXT_LIGHT};
                border: 1px solid #1976D2;
                border-radius: 3px;
            }}
            QPushButton:hover {{
                background-color: {FlexGUIColors.READ_BTN_HOVER};
            }}
        """)
        self.btn_read_all.clicked.connect(self._on_read_all)
        layout.addWidget(self.btn_read_all)
        
        # Write All button
        self.btn_write_all = QPushButton("Write All")
        self.btn_write_all.setFixedSize(75, 26)
        self.btn_write_all.setFont(QFont("Segoe UI", 8))
        self.btn_write_all.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_write_all.setStyleSheet(f"""
            QPushButton {{
                background-color: {FlexGUIColors.WRITE_BTN_BG};
                color: {FlexGUIColors.TEXT_LIGHT};
                border: 1px solid #3d8b40;
                border-radius: 3px;
            }}
            QPushButton:hover {{
                background-color: {FlexGUIColors.WRITE_BTN_HOVER};
            }}
        """)
        self.btn_write_all.clicked.connect(self._on_write_all)
        layout.addWidget(self.btn_write_all)
        
        return header
        
    def _create_register_callback(self, is_write: bool):
        """Create a callback function for register widgets"""
        def callback(register_view: RegisterViewWidget):
            if is_write and self._on_write_callback:
                self._on_write_callback(register_view)
            elif not is_write and self._on_read_callback:
                self._on_read_callback(register_view)
        return callback
        
    def _on_write_all(self):
        """Handle write all button - call write callback for each register"""
        if self._on_write_callback:
            for widget in self._register_widgets.values():
                self._on_write_callback(widget)
                
    def _on_read_all(self):
        """Handle read all button - call read callback for each register"""
        if self._on_read_callback:
            for widget in self._register_widgets.values():
                self._on_read_callback(widget)
        
    def set_callbacks(
        self,
        on_write: Callable[[RegisterViewWidget], None] = None,
        on_read: Callable[[RegisterViewWidget], None] = None
    ):
        """
        Set global callbacks for read/write operations.
        Callbacks receive the RegisterViewWidget instance.
        """
        if on_write:
            self._on_write_callback = on_write
        if on_read:
            self._on_read_callback = on_read
            
        # Update existing register widgets with new callbacks
        for widget in self._register_widgets.values():
            widget.set_callbacks(
                on_write=self._create_register_callback(True),
                on_read=self._create_register_callback(False)
            )
        
    def add_register(self, register_def: RegisterDefinition):
        """Add a register to the list"""
        if register_def.name in self._register_widgets:
            return  # Already exists
            
        # Remove stretch if it exists
        self.register_layout.takeAt(self.register_layout.count() - 1)
        
        # Create and add register widget with callbacks
        reg_widget = RegisterViewWidget(
            register_def,
            on_write_callback=self._create_register_callback(True),
            on_read_callback=self._create_register_callback(False)
        )
        
        self._register_widgets[register_def.name] = reg_widget
        self.register_layout.addWidget(reg_widget)
        
        # Re-add stretch
        self.register_layout.addStretch()
        
    def remove_register(self, name: str):
        """Remove a register from the list"""
        if name in self._register_widgets:
            widget = self._register_widgets.pop(name)
            self.register_layout.removeWidget(widget)
            widget.deleteLater()
            
    def clear_registers(self):
        """Clear all registers from the list"""
        for name in list(self._register_widgets.keys()):
            self.remove_register(name)
            
    def load_registers(self, registers: List[RegisterDefinition]):
        """Load a list of registers"""
        self.clear_registers()
        for reg_def in registers:
            self.add_register(reg_def)
            
    def get_register_widget(self, name: str) -> Optional[RegisterViewWidget]:
        """Get a register widget by name"""
        return self._register_widgets.get(name)
        
    def get_all_register_widgets(self) -> Dict[str, RegisterViewWidget]:
        """Get all register widgets"""
        return self._register_widgets.copy()
        
    def get_all_values(self) -> Dict[str, Tuple[int, int]]:
        """Get all register values as {name: (write_value, read_value)}"""
        result = {}
        for name, widget in self._register_widgets.items():
            result[name] = (widget.get_write_value(), widget.get_read_value())
        return result
        
    def set_write_value(self, name: str, value: int):
        """Set the write value for a register"""
        if name in self._register_widgets:
            self._register_widgets[name].set_write_value(value)
            
    def set_read_value(self, name: str, value: int):
        """Set the read value for a register"""
        if name in self._register_widgets:
            self._register_widgets[name].set_read_value(value)
            
    def set_all_read_values(self, values: Dict[str, int]):
        """Set read values for multiple registers"""
        for name, value in values.items():
            self.set_read_value(name, value)
            
    def set_all_write_values(self, values: Dict[str, int]):
        """Set write values for multiple registers"""
        for name, value in values.items():
            self.set_write_value(name, value)


# ============================================================================
# Demo Application
# ============================================================================

def run_demo():
    """Run a demo application to test the widget"""
    import sys
    
    app = QApplication(sys.argv)
    
    # Set application style
    app.setStyle('Fusion')
    
    # Create main window
    window = QMainWindow()
    window.setWindowTitle("GD3160 Register Map - FlexGUI Style")
    window.setGeometry(100, 100, 1000, 500)
    
    # Create register map widget with callbacks
    def on_write_callback(reg_view: RegisterViewWidget):
        print(f"Write: {reg_view.get_register_name()} = 0x{reg_view.get_write_value():03X}")
        # Simulate write - update read value to match
        reg_view.set_read_value(reg_view.get_write_value())
        
    def on_read_callback(reg_view: RegisterViewWidget):
        print(f"Read: {reg_view.get_register_name()}")
        # Simulate read with random value
        import random
        simulated = random.randint(0, 0x3FF)
        reg_view.set_read_value(simulated)
        print(f"  -> Read value: 0x{simulated:03X}")
    
    register_map = RegisterMapWidget(
        on_write_callback=on_write_callback,
        on_read_callback=on_read_callback
    )
    
    # Load GD3160 registers
    register_map.load_registers(GD3160_REGISTERS)
    
    window.setCentralWidget(register_map)
    window.show()
    
    sys.exit(app.exec_())


if __name__ == "__main__":
    run_demo()
