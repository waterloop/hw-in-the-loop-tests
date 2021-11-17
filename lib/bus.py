from __future__ import annotations
import can
import threading
import sys
from typing import Callable
from datetime import datetime
from frame import CANFrame

_BUSTYPE = "socketcan"

def _monitor_bus(bus_obj: CANBus):
    while (1):
        for msg in bus_obj._bus:
            frame = CANFrame(
                arb_id = msg.arbitration_id, payload = list(msg.data))

            # TODO: replace with python-can timestamps if
            #       this isn't goot enough
            dt_now = datetime.now()
            
            bus_obj._log_file.write(f"{dt_now}, {frame.arb_id}, {frame.payload}\n")
            bus_obj._rx_callback(frame, dt_now)

class CANBus():
    def __init__(self, interface):
        self._rx_callback = lambda *args: None
        self._bus = can.ThreadSafeBus(channel = interface, bustype = _BUSTYPE)
        self._monitor_bus_thread = threading.Thread(
            target = _monitor_bus, args = (self,), daemon = True)

        self._monitor_bus_thread.start()

    def __enter__(self):
        self._log_file = open(f"/tmp/{sys.argv[0].split('.')[0]}-{datetime.now().date()}.txt", 'a')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._log_file.close()

    def put_frame(self, frame: CANFrame):
        msg = can.Message(
            arbitration_id = frame.arb_id, data = frame.payload, is_extended_id = False)
        self._bus.send(msg)

    def set_rx_callback(self, callback: Callable):
        self._rx_callback = callback

    def send_canopen(self, node_id, is_query, empty_bytes, index, subindex, data):                                                                              
        byte_0 = 0b00000000 | ((4 if is_query else 2) << 4) | (empty_bytes << 2)      
        msg = can.Message(                                                            
            arbitration_id=0x600 + node_id,
            is_extended_id=False,
            data=[
                byte_0,
                (index >> (8 * 0)) & 0b11111111,
                (index >> (8 * 1)) & 0b11111111,
                subindex,
                (data >> (8 * 0)) & 0b11111111,
                (data >> (8 * 1)) & 0b11111111,
                (data >> (8 * 2)) & 0b11111111,
                (data >> (8 * 3)) & 0b11111111
            ]
        )

        self._bus.send(msg)

    def send_set_motor_command(self, node_id, motor, throttle_percent):
        self.send_canopen(
            node_id = node_id,
            is_query = False,
            empty_bytes = 0,
            index = 0x2000,
            subindex = motor,
            data = throttle_percent*10
        )
