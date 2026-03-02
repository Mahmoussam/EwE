"""
SerialDispatcher - Async/Await middleware layer for Serial Communication

This module provides an asyncio-based abstraction layer that sits between
the GUI and SerialWorker. It manages message correlation using Message IDs (MID),
assigns futures to outgoing messages, and resolves them when responses arrive.

Features:
- Async/await pattern for serial communication
- timeout exception raising
- Message correlation via MID
- Returns responses to original issuers
"""

import asyncio
from typing import Dict, Optional, Any
from PyQt5.QtCore import QObject, pyqtSlot

from .serial_messages import *
from .serial_utils import SerialWorker


class SerialDispatcher(QObject):
    """
    Async middleware between GUI and SerialWorker.
    
    Manages message correlation using sequential MIDs (Message IDs).
    Provides an async send_request API that resolves when a response
    with matching MID arrives, or raises TimeoutError.
    
    Usage:
        dispatcher = SerialDispatcher(serial_worker)
        response = await dispatcher.send_request(msg, timeout=2.0)
    """
    
    def __init__(self, worker: SerialWorker):
        """
        Initialize the SerialDispatcher.
        
        Args:
            worker: SerialWorker instance that handles actual serial I/O
        """
        super().__init__()
        self._worker = worker
        self._pending: Dict[int, asyncio.Future] = {}
        self._mid_counter: int = 0  # Private counter for generating message IDs
        
        # Connect to worker's data_received signal
        # This will be called in the GUI thread (Qt's signal mechanism)
        self._worker.data_received.connect(self._on_data_received)
    
    def _generate_mid(self) -> int:
        """
        Generate the next message ID using the dispatcher's internal counter.
        
        Returns:
            int: The next message ID (0-255, wraps around)
        """
        self._mid_counter += 1
        if self._mid_counter == 256:
            self._mid_counter = 0
        return self._mid_counter
    
    async def send_request(self, message: SerialMessage, timeout: float = 5.0) -> SerialMessage:
        """
        Send a request and await the response with timeout.
        
        This method:
        1. Generates a MID from the dispatcher's internal counter
        2. Assigns it to the message
        3. Creates a future for this MID
        4. Sends the message to SerialWorker
        5. Waits for response with specified timeout
        6. Returns the response or raises TimeoutError
        
        Args:
            message: SerialMessage to send (ReadMessage, WriteMessage, etc.)
            timeout: Timeout in seconds (default: 5.0)
            
        Returns:
            SerialMessage: The response message with matching MID
            
        Raises:
            asyncio.TimeoutError: If no response received within timeout period
        """
        loop = asyncio.get_running_loop()
        mid = self._generate_mid()
        message.MID_CNT = mid  # Assign the generated ID to the message
        
        # Create future for this message
        fut = loop.create_future()
        self._pending[mid] = fut
        
        # Send message to worker (queues it for transmission)
        self._worker.send_message(message)
        
        # Schedule timeout handler
        def _on_timeout():
            if not fut.done():
                fut.set_exception(asyncio.TimeoutError(
                    f"Timeout waiting for response to MID={mid} (cmd={message._cmd:#x})"
                ))
                self._pending.pop(mid, None)
        
        timeout_handle = loop.call_later(timeout, _on_timeout)
        
        try:
            # Wait for response
            result: SerialMessage = await fut
            return result
        finally:
            # Cancel timeout and cleanup
            timeout_handle.cancel()
            self._pending.pop(mid, None)
    
    async def read_register(self, addr: int, timeout: float = 5.0) -> int:
        """
        Convenience method to read a register and return its value.
        
        Args:
            addr: Register address to read
            timeout: Timeout in seconds
            
        Returns:
            int: The data value from the response
            
        Raises:
            asyncio.TimeoutError: If no response received within timeout
        """
        msg = ReadMessage(addr)
        response = await self.send_request(msg, timeout=timeout)
        return response._data
    
    async def write_register(self, addr: int, data: int, timeout: float = 5.0) -> SerialMessage:
        """
        Convenience method to write a register and await acknowledgment.
        
        Args:
            addr: Register address to write
            data: Data value to write
            timeout: Timeout in seconds
            
        Returns:
            SerialMessage: The response/acknowledgment message
            
        Raises:
            asyncio.TimeoutError: If no response received within timeout
        """
        msg = WriteMessage(addr, data)
        response = await self.send_request(msg, timeout=timeout)
        return response
    
    @pyqtSlot(object)
    def _on_data_received(self, msg: SerialMessage):
        """
        Called when SerialWorker receives a message (Qt signal handler).
        
        Resolves the corresponding future if one is waiting for this MID.        
        Args:
            msg: SerialMessage received from the device
        """
        try:
            mid = msg.MID_CNT
            
            # Check if anyone is waiting for this MID
            if mid in self._pending:
                fut = self._pending.pop(mid)
                if not fut.done():
                    # Resolve the future with the response
                    fut.set_result(msg)
            else:
                # No one waiting for this message
                # This could be an unsolicited message or a late response
                print(f"[SerialDispatcher] Unhandled message: {msg}")
                
        except Exception as e:
            print(f"[SerialDispatcher] Error in _on_data_received: {e}")
    
    def cancel_all_pending(self):
        """
        Cancel all pending requests.
        
        Useful during shutdown or when disconnecting from serial port.
        """
        for mid, fut in list(self._pending.items()):
            if not fut.done():
                fut.set_exception(asyncio.CancelledError(
                    f"Request cancelled (MID={mid})"
                ))
        self._pending.clear()
    
    @property
    def pending_count(self) -> int:
        """Get the number of pending requests."""
        return len(self._pending)
    
    def has_pending_request(self, mid: int) -> bool:
        """Check if a request with given MID is pending."""
        return mid in self._pending
