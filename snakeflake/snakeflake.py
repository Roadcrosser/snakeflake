"""Snakeflake Main Class"""

from exceptions import ExceededTimeException
import datetime
import math

class SnakeflakeGenerator:
    """The Snakeflake Generator"""

    def __init__(self, config:SnakeflakeGeneratorConfig):
        # Adjust snowflake constants
        self._timestamp_bits = config._timestamp_bits
        self._timescale = config._timescale
        self._serial_bits = config._serial_bits
        self._machine_id_bits = config._machine_id_bits

        # Set generator settings
        self.epoch = config.epoch
        self.machine_id = config.machine_id
        self.serial = 0

    def next_id(self):
        """Returns the next snakeflake ID"""

        timestamp = (datetime.datetime.utcnow() - epoch)
        timestamp /= datetime.timedelta(microseconds=1)
        timestamp /= self._timescale
        timestamp = math.floor(timestamp)

        if timestamp > 2 ** self._timestamp_bits:
            raise ExceededTimeException(f"Worker {self.machine_id}: Too much time has passed from the epoch to be able to generate a snakeflake.")
            return
        
        new_snakeflake = 0

        snakeflake_builder_components [
            (timestamp, self._serial_bits),
            (serial, self._machine_id_bits),
            (machine_id, 0)
        ]

        for value, bitcount in snakeflake_builder_components:
            new_snakeflake += value
            new_snakeflake << bitcount

        serial = (serial + 1) % 2 ** self._serial_bits

        return new_snakeflake
        
