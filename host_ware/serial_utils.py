import serial.tools.list_ports
from PyQt5.QtCore import QObject, QThread, pyqtSignal, pyqtSlot

def get_all_com_ports_names():
    names = []
    ports = serial.tools.list_ports.comports()
    for port in ports:
        names.append(port.device)
    return names

class SerialWorker(QObject):

    data_received = pyqtSignal(tuple)   # (cmd, data)
    status = pyqtSignal(bool)            # e.g. "Connected", "Disconnected"

    def __init__(self, port = "COM4" , baud = 9600):
        super().__init__()
        self.port = port
        self.baud = baud
        self._running = False
        self._ser = None
        self._tx_queue = []  # store outgoing commands temporarily

    @pyqtSlot()
    def start_serial(self):
        """Try to open the serial port and start reading loop."""
        try:
            self._ser = serial.Serial(self.port, self.baud, timeout=0.1)
            self._running = True
            self.status.emit(f"Connected to {self.port}")
            self.read_loop()
        except serial.SerialException as e:
            self.status.emit(f"Serial error: {e}")

    def read_loop(self):
        """Main loop: read incoming data and send queued commands."""
        while self._running:
            try:
                # Read line (example format: "CMD:DATA")
                line = self._ser.readline().decode(errors="ignore").strip()
                if line:
                    if ":" in line:
                        cmd, data = line.split(":", 1)
                    else:
                        cmd, data = "RAW", line
                    self.data_received.emit((cmd, data))

                # send queued outgoing commands
                if self._tx_queue:
                    to_send = self._tx_queue.pop(0)
                    self._ser.write((to_send + "\n").encode())

                time.sleep(0.02)

            except serial.SerialException:
                self.status.emit("Serial disconnected")
                self._running = False
                break

        if self._ser and self._ser.is_open:
            self._ser.close()
            self.status.emit("Serial closed")

    @pyqtSlot(str)
    def send_command(self, cmd):
        """Add command to transmission queue."""
        self._tx_queue.append(cmd)

    @pyqtSlot()
    def stop(self):
        """Stop worker loop."""
        self._running = False