''' Serial Commands So far:
    
    1      ACKnowledge
    2      Write Addr Data
    3      Read  Addr 0

    # raw binary (example format: "!CADD")  C for cmd , D for data..
'''

class SerialMessage():
    ''' Base Class for Serial Messages '''
    CMD_LEN  = 1
    ADDR_LEN = 1
    DATA_LEN = 2
    MSG_LEN  = 1 + CMD_LEN + ADDR_LEN + DATA_LEN
    SERIAL_DELI = b'!' # takes 1 byte
    
    def __init__(self):
        self._cmd  = 0x0
        self._addr = 0x0
        self._data = 0x0
    def to_bytes(self):
        msg = self.SERIAL_DELI
        msg += self._cmd.to_bytes(self.CMD_LEN , 'big')
        msg += self._addr.to_bytes(self.ADDR_LEN , 'big')
        msg += self._data.to_bytes(self.DATA_LEN , 'big')
        return msg
    def __repr__(self):
        return f"<SerialMessage cmd={self._cmd:#x}, addr={self._addr:#x}, data={self._data:#x}>"
    
    @classmethod
    def from_bytes(cls, data: bytes):
        if data[0:1] != cls.SERIAL_DELI:
            raise ValueError("Invalid delimiter")
        cmd  = data[1]
        addr = data[2]
        data  = int.from_bytes(data[3:5], 'big')
        return cls(cmd, addr, data)
    
class AcknowledgeMessage(SerialMessage):
    def __init__(self):
        super().__init__()
        self._cmd  = 1
        self._addr = 0xFF
        self._data = 0xFFFF

class WriteMessage(SerialMessage):
    def __init__(self , addr , data):
        super().__init__()
        self._cmd  = 2
        self._addr = addr
        self._data   = data

class WriteMessage(SerialMessage):
    def __init__(self , addr , data):
        super().__init__()
        self._cmd  = 2
        self._addr = addr
        self._data   = data
class ReadMessage(SerialMessage):
    def __init__(self , addr):
        super().__init__()
        self._cmd  = 3
        self._addr = addr
        self._data   = 0
