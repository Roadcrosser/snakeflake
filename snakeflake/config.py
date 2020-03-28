"""Snakeflake Configuration"""

import datetime
from snakeflake.utils import get_ip, ipv4_to_int, world_epoch


class SnakeflakeConstants:
    """
    The Snakeflake Config class that deals with constants
    
    The default values were taken from https://github.com/sony/sonyflake.

    You can change them to suit your needs if you need to, I suppose.
    """

    def __init__(self, timestamp_bits, timescale, serial_bits, machine_id_bits):
        self.timestamp_bits = timestamp_bits
        self.timescale = timescale
        self.serial_bits = serial_bits
        self.machine_id_bits = machine_id_bits

    @classmethod
    def defaults(cls):
        return cls(39, 10000, 8, 16)


class SnakeflakeGeneratorConfig:
    """The Snakeflake Generator Config class"""

    def __init__(
        self,
        epoch: datetime.datetime = None,
        machine_id: int = None,
        constants: SnakeflakeConstants = None,
        timestamp_method=None,
    ):
        if epoch == None:
            epoch = world_epoch()

        if constants == None:
            constants = SnakeflakeConstants.defaults()

        if machine_id == None:
            machine_id = ipv4_to_int(get_ip(), constants.machine_id_bits)

        if timestamp_method == None:
            timestamp_method = datetime.datetime.utcnow

        self.epoch = epoch
        self.machine_id = machine_id
        self.constants = constants
        self.timestamp_method = timestamp_method
