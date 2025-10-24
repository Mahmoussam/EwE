''' Serial Commands So far:
    
    1      ACKnowledge
    2      Write Addr Data
    3      Read  Addr 0

    # raw binary (example format: "!CADDI")  C for cmd , D for data , I for ID
'''

class SerialMessage():
    ''' Base Class for Serial Messages '''
    SERIAL_DELI = b'!' # takes 1 byte
    CMD_LEN  = 1
    ADDR_LEN = 1
    DATA_LEN = 2
    MID_LEN  = 1
    MSG_LEN  = len(SERIAL_DELI) + CMD_LEN + ADDR_LEN + DATA_LEN + MID_LEN
    
    MID_CNT = 0
    
    def __init__(self , cmd  = 0 , addr = 0 , data = 0):
        self._cmd  = cmd
        self._addr = addr
        self._data = data
        SerialMessage.MID_CNT += 1
        if SerialMessage.MID_CNT == 256:
            SerialMessage.MID_CNT = 0
        self.MID_CNT = SerialMessage.MID_CNT

    
    def to_bytes(self):
        msg = self.SERIAL_DELI
        msg += self._cmd.to_bytes(self.CMD_LEN , 'big')
        msg += self._addr.to_bytes(self.ADDR_LEN , 'big')
        msg += self._data.to_bytes(self.DATA_LEN , 'big')
        #print('zz' , msg)
        msg += self.MID_CNT.to_bytes(self.MID_LEN , 'big')
        #print('zz' , msg)
        return msg
    def __repr__(self):
        return f"<SerialMessage#{self.MID_CNT} cmd={self._cmd:#x}, addr={self._addr:#x}, data={self._data:#x}>"
    
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
    def __repr__(self):
        return f"<ACK Message#{self.MID_CNT} cmd={self._cmd:#x}, addr={self._addr:#x}, data={self._data:#x}>"
    
class WriteMessage(SerialMessage):
    def __init__(self , addr , data):
        super().__init__()
        self._cmd  = 2
        self._addr = addr
        self._data   = data
    def __repr__(self):
        return f"<Write Message#{self.MID_CNT} cmd={self._cmd:#x}, addr={self._addr:#x}, data={self._data:#x}>"

class ReadMessage(SerialMessage):
    def __init__(self , addr):
        super().__init__()
        self._cmd  = 3
        self._addr = addr
        self._data   = 0
    def __repr__(self):
        return f"<Read Message#{self.MID_CNT} cmd={self._cmd:#x}, addr={self._addr:#x}>"