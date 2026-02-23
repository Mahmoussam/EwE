from PyQt5 import QtWidgets, uic
from PyQt5.QtGui import QPixmap
from E_Serial import ReadMessage
import os
from datetime import datetime


class GDStatusWindow(QtWidgets.QMainWindow):
    def __init__(self, serial_worker):
        """
        Initialize the GD3160 Status Window
        
        Args:
            serial_worker: Reference to the SerialWorker instance for sending messages
        """
        super().__init__()
        self.__serial_worker = serial_worker
        
        # Load the UI with absolute path
        ui_path = os.path.join(os.path.dirname(__file__), "UIs", "status_gui.ui")
        uic.loadUi(ui_path, self)
        
        # Set window properties
        self.setWindowTitle("GD3160 Status")
        
        # Connect button signals
        self.refresh_status_button.clicked.connect(self.__on_refresh_status_clicked)
        self.screenshot_button.clicked.connect(self.__on_screenshot_clicked)
        
    def __on_refresh_status_clicked(self):
        """Handle the Refresh Status button click"""
        print("[GDStatusWindow] Refreshing status...")
        
        if self.__serial_worker is None:
            print("[GDStatusWindow] ERROR: Serial worker is not available")
            return
        
        # Send read messages for status registers
        # You can modify this to read specific registers based on your GD3160 device
        # Example: Read register at address 0
        msg = ReadMessage(0)
        self.__serial_worker.send_message(msg)
        
        print("[GDStatusWindow] Status refresh request sent")
    
    def __on_screenshot_clicked(self):
        """Handle the Screenshot button click"""
        print("[GDStatusWindow] Taking screenshot...")
        
        try:
            # Get the screenshots directory
            screenshots_dir = os.path.join(os.path.dirname(__file__), "screenshots")
            
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
        