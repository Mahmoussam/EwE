from PyQt5 import QtWidgets, uic
import time
from serial_utils import *

class MyWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        # init private members
        self.__ComConnectionState = False


        uic.loadUi("UIs/main_gui.ui", self)

        # connect Buttons
        self.ComRefreshButton.clicked.connect(self.ComRefreshButton_clicked)
        self.ComConnectButton.clicked.connect(self.ComConnectButton_clicked)
        self.ComStopButton.clicked.connect(self.ComStopButton_clicked)
        
    def ComRefreshButton_clicked(self):
        print('Refreshing com ports..')
        self.ComPortscomboBox.clear()
        #t1 = time.time()
        names = get_all_com_ports_names()
        #t1 = time.time() - t1
        #print("T1 " , t1)
        self.ComPortscomboBox.addItems(names)

        
    def ComConnectButton_clicked(self):
        print('Connecting com ports')

        self.__ComConnectionState = True
        # update ui
        self.__handle_ComStopButton_state()
        self.setEnabled_DRW_Fields(True)
        
    def ComStopButton_clicked(self):
        print('Stopping serial com.')

        self.__ComConnectionState = False
        # update ui
        self.__handle_ComStopButton_state()
        self.setEnabled_DRW_Fields(False)
        
    def setEnabled_DRW_Fields(self , state = True):
        ''' Method to enable/disable the Direct Read Write Frame fields'''
        self.WriteValInput.setEnabled(state)
        self.WriteAddrInput.setEnabled(state)
        self.ReadAddrInput.setEnabled(state)
    def __handle_ComStopButton_state(self):
        ''' Private Method to handle the state of ComStop Button (Enabled/Disabled) according to `__ComConnectionState` '''
        
        self.ComStopButton.setEnabled(self.__ComConnectionState)
if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = MyWindow()
    window.show()
    app.exec_()