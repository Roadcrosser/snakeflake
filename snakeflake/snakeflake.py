"""Snakeflake Main Class"""

from snakeflake import config, exceptions, utils
import datetime
import math

class SnakeflakeGenerator:
    """The Snakeflake Generator"""

    def __init__(self, genconfig:config.SnakeflakeGeneratorConfig):
        # Define snowflake constants
        self.constants = genconfig.constants

        # Set generator settings
        self.epoch = genconfig.epoch
        self.machine_id = genconfig.machine_id
        self.timestamp_method = genconfig.timestamp_method

        self.serial = 0

        if self.machine_id > (2 ** self.constants.machine_id_bits):
            raise exceptions.ExceededBitsException(f"Worker {self.machine_id}: The machine ID exceeds the number of bits allocated.")
            return


    def next_snakeflake(self):
        """Returns the next snakeflake as an object"""
        now = self.timestamp_method()
        ret = Snakeflake.from_generator(now, self)

        self.serial += 1

        return ret


    def next_id(self):
        """Returns the next snakeflake ID"""
        return self.next_snakeflake().get_id()


    def next_id_ignore_warning():
        """Returns the next snakeflake ID but ignores any warnings that occur"""
        new_snakeflake = None
        try:
            new_snakeflake = next_id()
        except (exceptions.ExceededTimeException, exceptions.EpochFutureException):
            pass
        return new_snakeflake




class Snakeflake:
    """Defines a snakeflake"""

    def __init__(self, timestamp, epoch, serial, machine_id, constants:config.SnakeflakeConstants=None):
        self.timestamp = timestamp
        self.epoch = epoch
        self.serial = serial
        self.machine_id = machine_id

        if constants == None:
            constants = config.SnakeflakeConstants.default()
        
        self.constants = constants

        self.calculate_snakeflake()


    @classmethod
    def from_generator(cls, timestamp, generator:SnakeflakeGenerator):
        return cls(timestamp, generator.epoch, generator.serial, generator.machine_id, generator.constants)


    def get_id(self):
        return self.snakeflake_id


    def calculate_snakeflake(self):
        timestamp = (self.timestamp - self.epoch)
        timestamp /= datetime.timedelta(microseconds=1)
        timestamp /= self.constants.timescale
        timestamp = math.floor(timestamp)

        if timestamp < 0:
            raise exceptions.EpochFutureException(utils.format_error(self.machine_id, "The epoch is in the future."))
            return

        if timestamp > (2 ** self.constants.timestamp_bits):
            raise exceptions.ExceededTimeException(utils.format_error(self.machine_id, "Too much time has passed from the epoch to be able to generate a snakeflake."))
            return
        
        new_snakeflake = 0

        snakeflake_builder_components = [
            (timestamp, self.constants.serial_bits),
            (self.serial, self.constants.machine_id_bits),
            (self.machine_id, 0)
        ]

        for value, bitcount in snakeflake_builder_components:
            new_snakeflake += value
            new_snakeflake = new_snakeflake << bitcount

        self.serial = (self.serial + 1) % 2 ** self.constants.serial_bits

        self.snakeflake_id = new_snakeflake