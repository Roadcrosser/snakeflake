"""
Snakeflake Configuration

This module defines the classes related to configuring a Snakeflake generator.
"""

import datetime
from snakeflake.utils import get_ip, ipv4_to_int, world_epoch


class SnakeflakeConstants:
    """
    The Snakeflake Config class that deals with constants
    
    It is recommended to initialize this class using the :meth:`defaults`
    classmethod instead.

    Args:
        timestamp_bits (int): The number of bits to allocate for the timestamp.
        timescale (int): The timestamp precision in microseconds.
        serial_bits (int): The number of bits to allocate for the serial number.
        machine_id_bits (int): The number of bits to allocate for the machine ID.
    """

    def __init__(self, timestamp_bits, timescale, serial_bits, machine_id_bits):
        self.timestamp_bits = timestamp_bits
        self.timescale = timescale
        self.serial_bits = serial_bits
        self.machine_id_bits = machine_id_bits

    @classmethod
    def defaults(cls):
        """
        Initializes the constants with their default values.

        These default values were taken from https://github.com/sony/sonyflake.
        """
        return cls(39, 10000, 8, 16)


class SnakeflakeGeneratorConfig:
    """The class that holds the configuration Snakeflake Generator Config class
    
    Args:
        epoch (datetime.datetime): When to start generating snakeflakes from.
        machine_id (int): The machine ID of the generator.
        constants (int): The constants this generator uses.
        timestamp_method (builtin_function_or_method): The method to call
            to generate a timestamp. This method will be called with no
            arguments whenever a snakeflake is to be generated.
            Defaults to `datetime.datetime.utcnow`.
    """

    def __init__(
        self, epoch=None, machine_id=None, constants=None, timestamp_method=None,
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
