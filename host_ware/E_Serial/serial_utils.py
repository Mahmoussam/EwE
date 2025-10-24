''' Serial Commands So far:
    
    1      ACKnowledge
    2      Write Addr Val
    3      Read  Addr 0

    # raw binary (example format: "!CADD")  C for cmd , D for data..
'''

import serial.tools.list_ports
from PyQt5.QtCore import QObject, QThread, pyqtSignal, pyqtSlot
import time

from .utils import *
from .serial_messages import *


def get_all_com_ports_names():
    names = []
    ports = serial.tools.list_ports.comports()
    for port in ports:
        names.append(port.device)
    return names


class SerialWorker(QObject):
    ''' Worker thread that Handles MCU Serial communication sends/receives.
        Middle layer between UI main thread and slave hardware(mcu)'''
    data_received = pyqtSignal(SerialMessage)
    status = pyqtSignal(bool)            # e.g. "Connected", "Disconnected"

    def __init__(self, port = "COM3" , baud = 9600):
        super().__init__()
        self.port = port
        self.baud = baud
        self._running = False
        self._ser = None
        self._tx_queue = []  # store outgoing commands temporarily
        self.__buffer = b""
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
                # Read line (example format: "!CDDD")  C for cmd , D for data
                ''' Buffered stream reading, protocol fixed size'''
                feed = self._ser.read_all().strip()
                self.__buffer += feed
                # try to re-line if packet loss occurs , Can it happen ?!
                
                while len(self.__buffer) >= SerialMessage.MSG_LEN:
                    sidx = self.__buffer.find(SerialMessage.SERIAL_DELI)
                    if sidx == -1:
                        break
                    self.__buffer = self.__buffer[sidx:]
                    line = self.__buffer[:SerialMessage.MSG_LEN]
                    self.__buffer = self.__buffer[SerialMessage.MSG_LEN:]
                    self.__on_raw_message_received(line)

                # send queued outgoing commands
                if self._tx_queue:
                    print('[!] thread writing..')
                    to_send = self._tx_queue.pop(0)
                    try:
                        self.__send_message(to_send)
                    except Exception as ex:
                        print(RED_CMD , '[!] Wrong packet format: ',to_send ,f"\n {ex}" , WHITE_CMD)
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
    def send_message(self, msg : SerialMessage):
        """Add message to transmission queue."""
        self._tx_queue.append(msg)

    @pyqtSlot()
    def stop(self):
        """Stop worker loop."""
        self._running = False

    def __on_raw_message_received(self , raw_msg: bytes):
        ''' Callback handler on complete raw message received on serial '''
        print(raw_msg)
        self.data_received.emit(SerialMessage.from_bytes(raw_msg))
    def __send_message(self , to_send : SerialMessage):
        ''' Called on message object ready to be sent
            process the object to raw bytes and writes them to serial '''
        msg_bytes = to_send.to_bytes()
        print(YELLOW_CMD , '[*] Sending ' , msg_bytes , WHITE_CMD)
        self._ser.write(msg_bytes)
        self._ser.flush()