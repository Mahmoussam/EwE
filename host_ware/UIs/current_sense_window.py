from PyQt5 import QtWidgets, uic
import os

# Import compiled background images resources
try:
    from . import background_images_rc  # When imported as a module from UIs package
except ImportError:
    import background_images_rc  # When running standalone


class CurrentSenseWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        """Load and expose the current_sense.ui as a reusable widget."""
        super().__init__(parent)

        ui_path = os.path.join(os.path.dirname(__file__), "current_sense.ui")
        uic.loadUi(ui_path, self)

        self.setWindowTitle("Current Sense")


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    window = CurrentSenseWindow()
    window.show()
    sys.exit(app.exec_())
