from PyQt5 import QtWidgets, uic
import os

# Import compiled background images resources
try:
    from . import background_images_rc  # When imported as a module from UIs package
except ImportError:
    import background_images_rc  # When running standalone


class GateDriveWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        """Load and expose the gate_drive.ui as a reusable widget."""
        super().__init__(parent)

        ui_path = os.path.join(os.path.dirname(__file__), "gate_drive.ui")
        uic.loadUi(ui_path, self)

        self.setWindowTitle("Gate Drive")


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    window = GateDriveWindow()
    window.show()
    sys.exit(app.exec_())
