from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QThread
import time
import os
import sys
import asyncio
from qasync import QEventLoop, asyncSlot

from E_Serial import *
from UIs.gd_control_panel import GDControlPanel


class MyWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Run startup validation
        if not self.__startup_validation():
            sys.exit(1)
        
        # init private members
        self.__ComConnectionState = False
        self.__dchain_length = 1
        self.__sworker = None
        self.__dispatcher = None
        self.__thread  = None
        self.__status_windows = []
        # Load the UI with absolute path
        ui_path = os.path.join(os.path.dirname(__file__), "UIs", "main_gui.ui")
        uic.loadUi(ui_path, self)

        # connect Buttons
        # Comm 
        self.ComRefreshButton.clicked.connect(self.ComRefreshButton_clicked)
        self.ComConnectButton.clicked.connect(self.ComConnectButton_clicked)
        self.ComStopButton.clicked.connect(self.ComStopButton_clicked)

        # DRW - Use asyncSlot for async button handlers
        self.WriteValButton.clicked.connect(lambda: asyncio.create_task(self.__DRW_WriteValButton_clicked()))
        self.ReadValButton.clicked.connect(lambda: asyncio.create_task(self.__DRW_ReadValButton_clicked()))

        self.ReadAddrInput.returnPressed.connect(lambda: asyncio.create_task(self.__DRW_ReadValButton_clicked()))
        self.WriteValInput.returnPressed.connect(lambda: asyncio.create_task(self.__DRW_WriteValButton_clicked()))
        self.WriteAddrInput.returnPressed.connect(lambda: self.WriteValInput.setFocus())
        # initial ports scan
        self.ComRefreshButton_clicked()
        self.__sync_dchain_state()
        #self.__status_windows = [GDControlPanel(self.__dispatcher, daisyChainIndex=0)]
        #self.__status_windows[0].show()
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
            "UIs/gd_control_panel.ui": "GD Control Panel UI"
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
        self.__handle_WriteValButton_state()
        self.__handle_ReadValButton_state()
        self.__handle_DChainLengthSpinBox_state()
        self.__handle_DXComboBox_state()
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

    async def __DRW_WriteValButton_clicked(self):
        '''Async handler for Write button - sends write request and awaits response'''
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
        
        if self.__dispatcher is None or self.__sworker is None:
            print(RED_CMD , 'Serial not connected!' , WHITE_CMD)
            return
        
        # Use dispatcher to send and await response
        try:
            dx = self.__get_selected_dx()
            response = await self.__dispatcher.write_register(addr, val, timeout=2.0, dx=dx)
            print(f'[✓] Write successful: {response}')
        except asyncio.TimeoutError:
            print(RED_CMD , f'[✗] Write timeout for addr {addr:#x}' , WHITE_CMD)
        except Exception as ex:
            print(RED_CMD , f'[✗] Write error: {ex}' , WHITE_CMD)
        
    async def __DRW_ReadValButton_clicked(self):
        '''Async handler for Read button - sends read request and awaits response'''
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
        
        if self.__dispatcher is None or self.__sworker is None:
            print(RED_CMD , 'Serial not connected!' , WHITE_CMD)
            return
        
        # Use dispatcher to send and await response
        try:
            dx = self.__get_selected_dx()
            data = await self.__dispatcher.read_register(addr, timeout=2.0, dx=dx)
            print(f'[✓] Read successful: addr={addr:#x}, data={data:#x}')
            self.ReadValOutput.setText(hex(data))
        except asyncio.TimeoutError:
            print(RED_CMD , f'[✗] Read timeout for addr {addr:#x}' , WHITE_CMD)
            self.ReadValOutput.setText('TIMEOUT')
        except Exception as ex:
            print(RED_CMD , f'[✗] Read error: {ex}' , WHITE_CMD)
            self.ReadValOutput.setText('ERROR')
        
    def __setEnabled_DRW_Fields(self , state = True):
        ''' Method to enable/disable the Direct Read Write Frame fields'''
        self.WriteValInput.setEnabled(state)
        self.WriteAddrInput.setEnabled(state)
        self.ReadAddrInput.setEnabled(state)

    def __handle_DChainLengthSpinBox_state(self):
        ''' Private Method to handle the state of DChainLengthSpinBox (Enabled/Disabled) according to `__ComConnectionState` '''
        self.DChainLengthSpinBox.setEnabled(not self.__ComConnectionState)

    def __handle_DXComboBox_state(self):
        ''' Private Method to handle the state of DXComboBox (Enabled/Disabled) according to `__ComConnectionState` '''
        self.DXComboBox.setEnabled(self.__ComConnectionState)

    def __sync_dchain_state(self):
        '''Rebuild DXComboBox items from the current chain length.'''
        current_dx = self.DXComboBox.currentIndex()
        self.DXComboBox.blockSignals(True)
        self.DXComboBox.clear()
        for dx in range(self.__dchain_length):
            self.DXComboBox.addItem(str(dx), dx)
        self.DXComboBox.blockSignals(False)

    def __get_selected_dx(self):
        '''Return the selected daisy-chain index from the combo box.'''
        dx = self.DXComboBox.currentData()
        if dx is None:
            return 0
        return int(dx)

    def __handle_ComStopButton_state(self):
        ''' Private Method to handle the state of ComStop Button (Enabled/Disabled) according to `__ComConnectionState` '''
        self.ComStopButton.setEnabled(self.__ComConnectionState)

    def __handle_WriteValButton_state(self):
        ''' Private Method to handle the state of ComStop Button (Enabled/Disabled) according to `__ComConnectionState` '''
        self.WriteValButton.setEnabled(self.__ComConnectionState)
        
    def __handle_ReadValButton_state(self):
        ''' Private Method to handle the state of ComStop Button (Enabled/Disabled) according to `__ComConnectionState` '''
        self.ReadValButton.setEnabled(self.__ComConnectionState)

    def __connect_to_Serial(self, port , baud_rate):
        ''' handles action of connecting to serial port , creates a thread and worker '''
    
        try:
            
            # init service
            self.__sworker = SerialWorker(port , baud_rate)
            self.__thread = QThread()
            self.__sworker.moveToThread(self.__thread)

            # Create dispatcher - it will handle data_received internally
            self.__dispatcher = SerialDispatcher(self.__sworker)
            
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
        self.__close_status_windows()
        if self.__dispatcher is not None:
            # Cancel all pending requests
            self.__dispatcher.cancel_all_pending()
            self.__dispatcher = None
        if self.__sworker is not None:
            self.__sworker.stop()
        if self.__thread is not None:
            self.__thread.quit()
            self.__thread.wait()
        self.__ComConnectionState = False

    def __close_status_windows(self):
        '''Close and clear all GD control panel windows.'''
        for window in self.__status_windows:
            window.close()
            window.deleteLater()
        self.__status_windows.clear()

    async def __query_mcu_dchain_length(self):
        '''Ask MCU for daisy-chain length using ACK addr=2 and print response.'''
        if self.__dispatcher is None:
            return
        try:
            response = await self.__dispatcher.send_request(AskDaisyChainLenghtMessage(), timeout=2.0)
            print(f"[Main] MCU reported daisy-chain length: {response._dx}")
        except asyncio.TimeoutError:
            print("[Main] Timeout while querying MCU daisy-chain length")
        except Exception as ex:
            print(f"[Main] Failed to query MCU daisy-chain length: {ex}")


    def __on_status_update(self , status):
        print('[!]__on status update' , status)
        if status:
            self.__ComConnectionState = True
            # Create and show one control panel per GD in the configured daisy chain.
            self.__close_status_windows()
            self.__dchain_length = int(self.DChainLengthSpinBox.value())
            self.__sync_dchain_state()
            time.sleep(1)
            #self.__sworker.send_message(AcknowledgeDaisyChainLenghtMessage(dchain_len=self.__dchain_length))
            asyncio.create_task(self.__dispatcher.send_request(AcknowledgeDaisyChainLenghtMessage(dchain_len=self.__dchain_length) , timeout=2.0))
            asyncio.create_task(self.__query_mcu_dchain_length())

            for daisy_index in range(self.__dchain_length):
                panel = GDControlPanel(self.__dispatcher, daisyChainIndex=daisy_index)
                panel.show()
                self.__status_windows.append(panel)
            
        else:
            self.__ComConnectionState = False
            # Terminate control panels if they exist
            self.__close_status_windows()
        self.__refresh_ui()

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    
    # Set up asyncio event loop for qasync
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)
    
    window = MyWindow()
    window.show()
    
    with loop:
        loop.run_forever()