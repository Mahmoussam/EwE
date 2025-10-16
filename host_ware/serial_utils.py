CMD_LEN  = 3
DATA_LEN = 3
MSG_LEN = CMD_LEN + DATA_LEN
SERIAL_DELI = '!'

import serial.tools.list_ports
from PyQt5.QtCore import QObject, QThread, pyqtSignal, pyqtSlot
import time

def get_all_com_ports_names():
    names = []
    ports = serial.tools.list_ports.comports()
    for port in ports:
        names.append(port.device)
    return names

class SerialWorker(QObject):
    ''' Handles MCU Serial communication '''
    data_received = pyqtSignal(str)   # (cmd, data)
    status = pyqtSignal(bool)            # e.g. "Connected", "Disconnected"

    def __init__(self, port = "COM4" , baud = 9600):
        super().__init__()
        self.port = port
        self.baud = baud
        self._running = False
        self._ser = None
        self._tx_queue = []  # store outgoing commands temporarily
        self.__buffer = ""
    @pyqtSlot()
    def start_serial(self):
        """Try to open the serial port and start reading loop."""
        try:
            self._ser = serial.Serial(self.port, self.baud, timeout=0.1)
            self._running = True
            self.status.emit(True)
            
            self.read_loop()
        except serial.SerialException as e:
            print(f"\033[1;31mSerial error: {e}.\033[0m")
            self.status.emit(False)

    def read_loop(self):
        """Main loop: read incoming data and send queued commands."""
        while self._running:
            try:
                # Read line (example format: "CMD,DATA\r\n")
                ''' Buffered stream reading, protocol fixed size'''
                feed = self._ser.read_all().decode(encoding = "ascii", errors='ignore').strip()
                self.__buffer += feed
                # try to re-line if packet loss occurs , Can it happen ?!
                sidx = self.__buffer.find(SERIAL_DELI)
                if sidx != -1:
                    self.__buffer = self.__buffer[sidx:]
                while len(self.__buffer) >= MSG_LEN:
                    line = self.__buffer[:MSG_LEN]
                    self.__buffer = self.__buffer[MSG_LEN:]
                    self.data_received.emit(line)

                # send queued outgoing commands
                if self._tx_queue:
                    print('[!] thread writing..')
                    to_send = self._tx_queue.pop(0)
                    self._ser.write((to_send + "\n").encode())
                    self._ser.flush()

                time.sleep(0.02)

            except serial.SerialException as ex:
                print(f"\033[1;31mSerial Disconnected {ex}.\033[0m")
                self.status.emit(False)
                self._running = False
                break
            except Exception as ex:
                print(f"\033[1;31mSerial Exception {ex}.\033[0m")
                self.status.emit(False)
                self._running = False
                break
        if self._ser and self._ser.is_open:
            self._ser.close()
            print(f"\033[1;33mSerial Closed.\033[0m")
            self.status.emit(False)

    @pyqtSlot(str)
    def send_command(self, cmd):
        """Add command to transmission queue."""
        self._tx_queue.append(cmd)

    @pyqtSlot()
    def stop(self):
        """Stop worker loop."""
        self._running = False