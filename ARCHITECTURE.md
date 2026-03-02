# Serial Communication Architecture

## Overview

The application uses a layered architecture for serial communication with async/await support:

```
┌─────────────────────┐
│   GUI (main_c.py)   │  ← User interface layer
└──────────┬──────────┘
           │ async/await
           ↓
┌─────────────────────┐
│  SerialDispatcher   │  ← Async middleware layer
└──────────┬──────────┘
           │ Qt Signals
           ↓
┌─────────────────────┐
│   SerialWorker      │  ← Serial I/O worker (runs in QThread)
└──────────┬──────────┘
           │ pySerial
           ↓
┌─────────────────────┐
│   Serial Port       │  ← Hardware communication
└─────────────────────┘
```

## Components

### 1. SerialMessage (`E_Serial/serial_messages.py`)
- Base class for all serial messages
- Automatically generates sequential Message IDs (MID)
- Provides serialization/deserialization (`to_bytes()` / `from_bytes()`)
- Subclasses: `ReadMessage`, `WriteMessage`, `AcknowledgeMessage`

### 2. SerialWorker (`E_Serial/serial_utils.py`)
- Runs in a separate QThread
- Handles low-level serial I/O operations
- Maintains TX queue for outgoing messages
- Emits Qt signals:
  - `data_received(SerialMessage)` - when a message is received
  - `status(bool)` - connection status updates

### 3. SerialDispatcher (`E_Serial/serial_dispatcher.py`) **[NEW]**
- **Async middleware layer** between GUI and SerialWorker
- Manages message correlation using MID (Message ID)
- Provides async/await API for serial communication
- Features:
  - Automatic timeout handling
  - Future-based message correlation
  - Returns responses to original callers
  - Cancellation of pending requests on disconnect

#### Key Methods:
```python
async def send_request(message: SerialMessage, timeout: float = 2.0) -> SerialMessage
async def read_register(addr: int, timeout: float = 2.0) -> int
async def write_register(addr: int, data: int, timeout: float = 2.0) -> SerialMessage
```

### 4. Main GUI (`main_c.py`)
- Uses `qasync` for asyncio integration with Qt
- Button handlers are now async methods
- Awaits responses directly instead of tracking message IDs manually
- Handles timeout exceptions gracefully

## Message Flow Example

### Read Operation Flow:

1. **User clicks "Read" button**
   ```python
   async def __DRW_ReadValButton_clicked(self):
       data = await self.__dispatcher.read_register(addr=0x05, timeout=2.0)
   ```

2. **SerialDispatcher creates message and future**
   - Creates `ReadMessage(addr=0x05)` with MID=17
   - Creates `asyncio.Future` and stores it: `_pending[17] = future`
   - Sends message to SerialWorker via `send_message()`
   - Schedules timeout handler (2.0 seconds)

3. **SerialWorker transmits message**
   - Message queued in `_tx_queue`
   - Worker thread sends bytes to serial port
   - Example: `b'!\x03\x05\x00\x00\x11'` (delimiter, cmd, addr, data, MID)

4. **Device responds**
   - Serial port receives response bytes
   - SerialWorker parses into `SerialMessage` with MID=17
   - Emits `data_received(SerialMessage)` signal

5. **SerialDispatcher resolves future**
   - `_on_data_received()` called (Qt signal handler)
   - Finds `future = _pending.pop(17)`
   - Sets result: `future.set_result(response_message)`
   - Cancels timeout handler

6. **GUI receives result**
   - The `await` in step 1 returns with the response
   - GUI updates: `self.ReadValOutput.setText(hex(data))`

### Timeout Scenario:

If no response arrives within 2.0 seconds:
- Timeout handler fires
- Sets exception: `future.set_exception(asyncio.TimeoutError(...))`
- The `await` raises `asyncio.TimeoutError`
- GUI catches exception and displays error message

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python host_ware/main_c.py
```

Or use the batch file:
```bash
host_ware/run_designer.bat
```
## Notes

- Message IDs (MID) are 8-bit, wrapping from 0-255
- Default timeout is 2.0 seconds (configurable per request)
- The SerialDispatcher automatically cancels pending requests on disconnect
- Unhandled messages (no matching MID) are logged but not delivered
