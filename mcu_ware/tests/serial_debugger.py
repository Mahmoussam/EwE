import serial
import time
from datetime import datetime

PORT = "COM4"        # change to your port (e.g., "/dev/ttyUSB0" on Linux)
BAUD = 9600        # match Arduino baudrate

# Raw binary payload
payload = b"!\x03\x03\x00\x00\t"#b"\x21\x03\x03\x03\x03\x08"

def format_packet(data: bytes) -> str:
    # Hex view with spacing
    hex_view = " ".join(f"{b:02X}" for b in data)

    # ASCII view (printable chars only)
    ascii_view = "".join(chr(b) if 32 <= b <= 126 else "." for b in data)

    return f"""
[{datetime.now().strftime('%H:%M:%S.%f')[:-3]}]
Bytes: {len(data)}
HEX : {hex_view}
ASCII: {ascii_view}
----------------------------------------
""".strip()


with serial.Serial(PORT, BAUD, timeout=1) as ser:
    time.sleep(2)  # Arduino reset delay
    
    print("\n=== TRANSMIT =====================================")
    print(format_packet(payload))
    ser.write(payload)
    
    #ser.write(6)
    ser.flush()
    print("\nListening for responses...\n")

    while True:
        if ser.in_waiting:
            data = ser.read(ser.in_waiting)
            print("=== RECEIVE =====================================")
            print(format_packet(data))