from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QThread
import time
from serial_utils import *

class MyWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        # init private members
        self.__ComConnectionState = False
        self.__sworker = None
        self.__thread  = None

        uic.loadUi("UIs/main_gui.ui", self)

        # connect Buttons
        self.ComRefreshButton.clicked.connect(self.ComRefreshButton_clicked)
        self.ComConnectButton.clicked.connect(self.ComConnectButton_clicked)
        self.ComStopButton.clicked.connect(self.ComStopButton_clicked)


        # initial ports scan
        self.ComRefreshButton_clicked()
        
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

        if self.__connect_to_Serial():
            #success
            pass
        else:
            pass
        
        
        
    def ComStopButton_clicked(self):
        print('Stopping serial com.')

        self.__disconnect_serial()
        # update ui
        self.__refresh_ui()
        
    def __setEnabled_DRW_Fields(self , state = True):
        ''' Method to enable/disable the Direct Read Write Frame fields'''
        self.WriteValInput.setEnabled(state)
        self.WriteAddrInput.setEnabled(state)
        self.ReadAddrInput.setEnabled(state)

    def __handle_ComStopButton_state(self):
        ''' Private Method to handle the state of ComStop Button (Enabled/Disabled) according to `__ComConnectionState` '''
        
        self.ComStopButton.setEnabled(self.__ComConnectionState)

    def __connect_to_Serial(self):
        ''' handles action of connecting to serial port , creates a thread and worker '''
    
        try:
            # get data
            port = self.ComPortscomboBox.currentText()
            baud_rate = int(self.baudrateInput.text())
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

    def __on_data_received(self , data):
        print("[!]__on data received" , data)
        pass
    def __on_status_update(self , status):
        print('[!]__on status update' , status)
        if status:
            self.__ComConnectionState = True
            pass
        else:
            self.__ComConnectionState = False
            pass#hmmm...
        self.__refresh_ui()

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = MyWindow()
    window.show()
    app.exec_()