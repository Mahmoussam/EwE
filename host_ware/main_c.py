from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QThread
import time
import os
import sys

from E_Serial import *
from status_window import GDStatusWindow


class MyWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Run startup validation
        if not self.__startup_validation():
            sys.exit(1)
        
        # init private members
        self.__ComConnectionState = False
        self.__sworker = None
        self.__thread  = None
        self.__last_read_message_cid = -1
        self.__status_window = None
        # Load the UI with absolute path
        ui_path = os.path.join(os.path.dirname(__file__), "UIs", "main_gui.ui")
        uic.loadUi(ui_path, self)

        # connect Buttons
        # Comm 
        self.ComRefreshButton.clicked.connect(self.ComRefreshButton_clicked)
        self.ComConnectButton.clicked.connect(self.ComConnectButton_clicked)
        self.ComStopButton.clicked.connect(self.ComStopButton_clicked)

        # DRW
        self.WriteValButton.clicked.connect(self.__DRW_WriteValButton_clicked)
        self.ReadValButton.clicked.connect(self.__DRW_ReadValButton_clicked)

        self.ReadAddrInput.returnPressed.connect(self.__DRW_ReadValButton_clicked)
        self.WriteValInput.returnPressed.connect(self.__DRW_WriteValButton_clicked)
        self.WriteAddrInput.returnPressed.connect(lambda: self.WriteValInput.setFocus())
        # initial ports scan
        self.ComRefreshButton_clicked()
        
    def __startup_validation(self):
        """Validate that all required directories and files exist"""
        base_dir = os.path.dirname(__file__)
        
        # Create required directories if they don't exist
        dirs_to_create = ["icons", "screenshots"]
        for dir_name in dirs_to_create:
            dir_path = os.path.join(base_dir, dir_name)
            if not os.path.exists(dir_path):
                try:
                    os.makedirs(dir_path)
                    print(f"[Startup] Created directory: {dir_path}")
                except Exception as ex:
                    print(f"[Startup] ERROR: Failed to create directory {dir_path}: {ex}")
                    QtWidgets.QMessageBox.critical(None, "Startup Error", f"Failed to create directory: {dir_path}")
                    return False
        
        # Check if required UI files exist
        required_ui_files = {
            "UIs/main_gui.ui": "Main window UI",
            "UIs/status_gui.ui": "Status window UI"
        }
        
        missing_files = []
        for ui_file, description in required_ui_files.items():
            ui_path = os.path.join(base_dir, ui_file)
            if not os.path.exists(ui_path):
                missing_files.append(ui_file)
        
        if missing_files:
            error_msg = "Missing files:\n" + "\n".join(missing_files)
            print(f"[Startup] ERROR: {error_msg}")
            QtWidgets.QMessageBox.critical(None, "Missing Files", error_msg)
            return False
        
        print("[Startup] All validation checks passed")
        return True
        
    def ComRefreshButton_clicked(self):
        print('Refreshing com ports..')
        self.ComPortscomboBox.clear()
        #t1 = time.time()
        names = get_all_com_ports_names()
        #t1 = time.time() - t1
        #print("T1 " , t1)
        self.ComPortscomboBox.addItems(names)

    def __refresh_ui(self):
        self.__setEnabled_DRW_Fields(self.__ComConnectionState)
        self.__handle_ComStopButton_state()

    def ComConnectButton_clicked(self):
        print('Connecting com ports')
        # if previous worker alive , stop it!
        self.__disconnect_serial()
        try:    
            # get data
            port = self.ComPortscomboBox.currentText()
            baud_rate = int(self.baudrateInput.text())
        except Exception as ex:
            print(RED_CMD , f"Can't parse port/baud input: {ex}" , WHITE_CMD)
            return
        if self.__connect_to_Serial(port , baud_rate):
            #success
            pass
        else:
            pass
        
        
        
    def ComStopButton_clicked(self):
        print('Stopping serial com.')

        self.__disconnect_serial()
        # update ui
        self.__refresh_ui()

    def __DRW_WriteValButton_clicked(self):
        print('Write button clicked')
        addr = self.WriteAddrInput.text()
        val  = self.WriteValInput.text()
        try:
            try:
                addr = int(addr , 0)
            except ValueError:
                addr = str_to_register3160_addr(addr)
            if addr.bit_length() > 5:
                raise ValueError("Addr size > 5 bits, check GD3160 specs")
        except ValueError as ex:
            print(RED_CMD , f'Failed to parse Addr: {ex}' , WHITE_CMD)
            return
        try:
            val = int(val , 0)
            if val.bit_length() > 10:
                raise ValueError("Val size > 10 bits, check GD3160 specs")
        except ValueError as ex:
            print(RED_CMD , f'Failed to parse Val: {ex}' , WHITE_CMD)
            return
        
        if self.__sworker is None:
            return
        msg = WriteMessage(addr , val)
        self.__sworker.send_message(msg)
        
    def __DRW_ReadValButton_clicked(self):
        print('Read button clicked')
        addr = self.ReadAddrInput.text()
        try:
            try:
                addr = int(addr , 0)
            except ValueError:
                addr = str_to_register3160_addr(addr)
            if addr.bit_length() > 5:
                raise ValueError("Addr size > 5 bits, check GD3160 specs")
        except ValueError as ex:
            print(RED_CMD , f'Failed to parse Addr: {ex}' , WHITE_CMD)
            return
        if self.__sworker is None:
            return
        
        msg = ReadMessage(addr)

        self.__last_read_message_cid = msg.MID_CNT
        
        self.__sworker.send_message(msg)
        
    def __setEnabled_DRW_Fields(self , state = True):
        ''' Method to enable/disable the Direct Read Write Frame fields'''
        self.WriteValInput.setEnabled(state)
        self.WriteAddrInput.setEnabled(state)
        self.ReadAddrInput.setEnabled(state)

    def __handle_ComStopButton_state(self):
        ''' Private Method to handle the state of ComStop Button (Enabled/Disabled) according to `__ComConnectionState` '''
        
        self.ComStopButton.setEnabled(self.__ComConnectionState)

    def __connect_to_Serial(self, port , baud_rate):
        ''' handles action of connecting to serial port , creates a thread and worker '''
    
        try:
            
            # init serice
            self.__sworker = SerialWorker(port , baud_rate)
            self.__thread = QThread()
            self.__sworker.moveToThread(self.__thread)

            self.__sworker.data_received.connect(self.__on_data_received)
            self.__sworker.status.connect(self.__on_status_update)

            self.__thread.finished.connect(self.__sworker.deleteLater)
            # start service
            self.__thread.started.connect(self.__sworker.start_serial)
            self.__thread.start()


            
        except Exception as ex:
            print(f"\033[1;31m Connecting to Serial error: {ex}.\033[0m")
            return False
        return True

    def closeEvent(self, event):
        """Graceful shutdown."""
        self.__disconnect_serial()
        event.accept()

    def __disconnect_serial(self):
        ''' Disconnects serial connection and kills thread/serial worker '''
        if self.__sworker is not None:
            self.__sworker.stop()
            self.__thread.quit()
            self.__thread.wait()
        self.__ComConnectionState = False

    def __on_data_received(self , msg : SerialMessage):
        print("[!]__on data received" , msg)
        # Handle the event
        # print(msg.MID_CNT , self.__last_read_message_cid)
        if msg.MID_CNT == self.__last_read_message_cid:
            self.ReadValOutput.setText(hex(msg._addr))
        pass
    def __on_status_update(self , status):
        print('[!]__on status update' , status)
        if status:
            self.__ComConnectionState = True
            # Create and show a new status window
            self.__status_window = GDStatusWindow(self.__sworker)
            self.__status_window.show()
        else:
            self.__ComConnectionState = False
            # Terminate status window if it exists
            if self.__status_window is not None:
                self.__status_window.close()
                self.__status_window.deleteLater()
                self.__status_window = None
        self.__refresh_ui()

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = MyWindow()
    window.show()
    app.exec_()