from PyQt5 import QtWidgets, uic
from E_Serial import ReadMessage


class GDStatusWindow(QtWidgets.QMainWindow):
    def __init__(self, serial_worker):
        """
        Initialize the GD3160 Status Window
        
        Args:
            serial_worker: Reference to the SerialWorker instance for sending messages
        """
        super().__init__()
        self.__serial_worker = serial_worker
        
        # Load the UI
        uic.loadUi("UIs/status_gui.ui", self)
        
        # Set window properties
        self.setWindowTitle("GD3160 Status")
        