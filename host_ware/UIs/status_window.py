from PyQt5 import QtWidgets, uic
from PyQt5.QtGui import QPixmap
from E_Serial import ReadMessage
import os
import asyncio
from datetime import datetime


class GDStatusWindow(QtWidgets.QMainWindow):
    def __init__(self, serial_dispatcher):
        """
        Initialize the GD3160 Status Window
        
        Args:
            serial_dispatcher: Reference to the SerialDispatcher instance for async messaging
        """
        super().__init__()
        self.__dispatcher = serial_dispatcher
        
        # Load the UI with absolute path
        ui_path = os.path.join(os.path.dirname(__file__), "status_gui.ui")
        uic.loadUi(ui_path, self)
        
        # Set window properties
        self.setWindowTitle("GD3160 Status")
        
        # Connect button signals - use async for refresh button
        self.refresh_status_button.clicked.connect(
            lambda: asyncio.create_task(self.__on_refresh_status_clicked())
        )
        self.screenshot_button.clicked.connect(self.__on_screenshot_clicked)
        
    async def __on_refresh_status_clicked(self):
        """Handle the Refresh Status button click (async)"""
        print("[GDStatusWindow] Refreshing status...")
        
        if self.__dispatcher is None:
            print("[GDStatusWindow] ERROR: Serial dispatcher is not available")
            return
        
        # Send read messages for status registers
        # You can modify this to read specific registers based on your GD3160 device
        # Example: Read register at address 0
        try:
            data = await self.__dispatcher.read_register(0, timeout=2.0)
            print(f"[GDStatusWindow] Status register 0: {data:#x}")
            # Update UI with the received data
            # TODO: Add UI elements to display register values
        except asyncio.TimeoutError:
            print("[GDStatusWindow] ERROR: Timeout reading status register")
        except Exception as ex:
            print(f"[GDStatusWindow] ERROR: {ex}")
        
        print("[GDStatusWindow] Status refresh complete")
    
    def __on_screenshot_clicked(self):
        """Handle the Screenshot button click"""
        print("[GDStatusWindow] Taking screenshot...")
        
        try:
            # Get the screenshots directory
            screenshots_dir = os.path.join(os.path.dirname(__file__), "..", "screenshots")
            
            # Generate timestamp for filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_path = os.path.join(screenshots_dir, f"status_{timestamp}.png")
            
            # Take screenshot of the window
            pixmap = self.grab()
            
            # Save the screenshot
            if pixmap.save(screenshot_path):
                print(f"[GDStatusWindow] Screenshot saved to: {screenshot_path}")
                QtWidgets.QMessageBox.information(self, "Success", f"Screenshot saved to:\n{screenshot_path}")
            else:
                print(f"[GDStatusWindow] ERROR: Failed to save screenshot")
                QtWidgets.QMessageBox.critical(self, "Error", "Failed to save screenshot")
                
        except Exception as ex:
            print(f"[GDStatusWindow] ERROR taking screenshot: {ex}")
            QtWidgets.QMessageBox.critical(self, "Error", f"Error taking screenshot: {ex}")
        