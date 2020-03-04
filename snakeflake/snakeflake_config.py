"""Snakeflake Configuration"""

import datetime
from snakeflake.utils import get_ip, ipv4_to_int

class SnakeflakeConstantConfig:
    """
    The Snakeflake Config class that deals with constants
    
    These values were taken from https://github.com/sony/sonyflake.

    You can change them to suit your needs if you need to, I suppose.
    """

    def __init__(self):
        self._timestamp_bits = 39
        self._timescale = 10000
        self._serial_bits = 8
        self._machine_id_bits = 16

class SnakeflakeGeneratorConfig(SnakeflakeConstantConfig):
    """The Snakeflake Generator Config class"""

    def __init__(self, epoch:datetime.datetime, machine_id:int=None):
        
        if machine_id == None:
            machine_id = ipv4_to_int(get_ip(), self._machine_id_bits)

        self.epoch = epoch
        self.machine_id = machine_id
