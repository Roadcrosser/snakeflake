"""Snakeflake Main Class"""

from snakeflake import config, exceptions, utils
import datetime
import math


class SnakeflakeGenerator:
    """The Snakeflake Generator"""

    def __init__(self, genconfig: config.SnakeflakeGeneratorConfig):
        # Define snowflake constants
        self.constants = genconfig.constants

        # Set generator settings
        self.epoch = genconfig.epoch
        self.machine_id = genconfig.machine_id
        self.timestamp_method = genconfig.timestamp_method

        self.serial = 0

        if self.machine_id > (2 ** self.constants.machine_id_bits):
            raise exceptions.ExceededBitsException(
                utils.format_error(
                    self.machine_id,
                    "The machine ID exceeds the number of bits allocated.",
                )
            )
            return

    def next_snakeflake(self):
        """Returns the next snakeflake as an object"""
        now = self.timestamp_method()
        ret = Snakeflake.from_generator(now, self)
        ret.calculate_snakeflake()

        self.serial += 1

        return ret

    def next_id(self):
        """Returns the next snakeflake ID"""
        return self.next_snakeflake().get_id()


class Snakeflake:
    """Defines a snakeflake"""

    def __init__(
        self,
        timestamp: datetime.datetime,
        serial: int,
        machine_id: int,
        epoch: datetime.datetime = None,
        constants: config.SnakeflakeConstants = None,
        snakeflake_id: int = None,
    ):
        self.timestamp = timestamp
        self.serial = serial
        self.machine_id = machine_id

        if epoch == None:
            epoch = utils.world_epoch()

        self.epoch = epoch

        if constants == None:
            constants = config.SnakeflakeConstants.defaults()

        self.constants = constants

        self.snakeflake_id = snakeflake_id

    def __eq__(self, other):
        return (
            abs(
                utils.timestamp_to_microseconds(self.timestamp)
                - utils.timestamp_to_microseconds(other.timestamp)
            )
            <= self.constants.timescale
            and self.serial == other.serial
            and self.machine_id == other.machine_id
            and self.snakeflake_id == other.snakeflake_id
        )

    def __ne__(self, other):
        return not self.__eq__(other)

    @classmethod
    def from_generator(cls, timestamp: datetime, generator: SnakeflakeGenerator):
        return cls(
            timestamp,
            generator.serial,
            generator.machine_id,
            generator.epoch,
            generator.constants,
            None,
        )

    @classmethod
    def from_snakeflake(
        cls,
        snakeflake_id: int,
        epoch: datetime = None,
        constants: config.SnakeflakeConstants = None,
    ):
        return cls(None, None, None, epoch, constants, snakeflake_id,)

    def reverse_calculate_snakeflake(self):
        """
        Calculates and populates snakeflake's members from the ID.
        Typically used with the `from_snakeflake` classmethod.
        """

        snakeflake_component_lengths = (
            self.constants.machine_id_bits,
            self.constants.serial_bits,
            self.constants.timestamp_bits,
        )

        w_snakeflake = self.snakeflake_id

        res = []

        for b in snakeflake_component_lengths:
            res += [w_snakeflake & utils.bitfill(b)]
            w_snakeflake = w_snakeflake >> b

        self.machine_id, self.serial, timestamp = res

        timestamp *= self.constants.timescale
        timestamp = datetime.timedelta(microseconds=timestamp)
        self.timestamp = self.epoch + timestamp

    def calculate_snakeflake(self):
        """Calculates a snakeflake"""
        timestamp = self.timestamp - self.epoch
        timestamp /= datetime.timedelta(microseconds=1)
        timestamp /= self.constants.timescale
        timestamp = math.floor(timestamp)

        if timestamp < 0:
            raise exceptions.EpochFutureException(
                utils.format_error(self.machine_id, "The epoch is in the future.")
            )
            return

        if timestamp > (2 ** self.constants.timestamp_bits):
            raise exceptions.ExceededTimeException(
                utils.format_error(
                    self.machine_id,
                    "Too much time has passed from the epoch to be able to generate a snakeflake.",
                )
            )
            return

        new_snakeflake = 0

        snakeflake_builder_components = [
            (timestamp, self.constants.serial_bits),
            (self.serial, self.constants.machine_id_bits),
            (self.machine_id, 0),
        ]

        for value, bitcount in snakeflake_builder_components:
            new_snakeflake += value
            new_snakeflake = new_snakeflake << bitcount

        self.serial = (self.serial + 1) % 2 ** self.constants.serial_bits

        self.snakeflake_id = new_snakeflake

    def calculate(self):
        """A generic "smart" calculation method that lets the user not have to worry which calculation method to use."""
        if self.snakeflake_id == None:
            self.calculate_snakeflake()
        else:
            self.reverse_calculate_snakeflake()

    def get_id(self):
        """Returns the snakeflake ID"""
        return self.snakeflake_id
