"""
Snakeflake Main Class

This module defines the Snakeflake Generator and Snakeflake classes.
"""

__all__ = ["SnakeflakeGenerator", "Snakeflake"]

from snakeflake import config, exceptions, utils
import datetime
import math


class SnakeflakeGenerator:
    """The Snakeflake generator.
    
    This class allows one to generate snakeflakes quickly and easily
    after initializing. It also manages serial number incrementing.

    Args:
        genconfig (SnakeflakeGeneratorConfig): The config to initialize the generator.
    
    Raises:
        ExceededBitsException: If the machine ID exceeds the number of bits allocated.
    """

    def __init__(self, genconfig):
        # Define snakeflake constants
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
        """Returns the next snakeflake as an object and increments the serial.
        
        Returns:
            Snakeflake: The snakeflake object
        
        Raises:
            ExceededTimeException: If too much time has passed to be able to generate a snakeflake.
            EpochFutureException: If the epoch is in the future.
        """
        now = self.timestamp_method()
        ret = Snakeflake.from_generator(now, self)
        ret.calculate_snakeflake()

        self.serial += 1

        return ret

    def next_id(self):
        """Calls :meth:`next_snakeflake` and returns the next snakeflake ID.
        
        Returns:
            int: The snakeflake ID.
        
        Raises:
            ExceededTimeException: If too much time has passed to be able to generate a snakeflake.
            EpochFutureException: If the epoch is in the future.
        """
        return self.next_snakeflake().get_id()


class Snakeflake:
    """Defines a snakeflake
    
    This class holds the attributes of a snakeflake and
    calculates the actual snakeflake ID.

    .. note::

        When instancing this class, please try to use the
        :meth:`from_generator` or :meth:`from_snowflake`
        classmethods to generate snakeflakes instead.

    Args:
        timestamp (datetime.datetime): The timestamp of the snakeflake.
        serial (int): The serial number of the snakeflake.
        machine_id (int): The machine ID of the snakeflake.
        epoch (datetime.datetime): When this snakeflake started counting from.
        constants (SnakeflakeConstants): The constants this snakeflake uses.
        snakeflake_id (int): The ID of this snakeflake.
            This should only be specified if you are deriving information from a snakeflake ID.
    """

    def __init__(
        self,
        timestamp,
        serial,
        machine_id,
        epoch=None,
        constants=None,
        snakeflake_id=None,
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
    def from_generator(cls, timestamp, generator):
        """
        Generates a snakeflake using data from the generator object.
        The snakeflake ID itself will not be calculated until :meth:`calculate_snakeflake` is run.

        .. warning::
            This will not increment the serial number of the generator itself.
            Please instead generate snakeflakes from the :class:`SnakeflakeGenerator` directly for this functionality.

        Args:
            timestamp (datetime.datetime): The timestamp of the snakeflake.
            generator (SnakeflakeGenerator): The generator with the data that will be used to generate the snakeflake.
        """
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
        cls, snakeflake_id, epoch=None, constants=None,
    ):
        """
        Generates a snakeflake from a snakeflake ID. This is usually
        used for deriving the timestamp of a snakeflake, although the
        serial and machine IDs will also be calculated.

        Note that the resulting attributes will not be calculated until
        :meth:`reverse_calculate_snakeflake` is run.

        Args:
            snakeflake_id (int): The snakeflake.
            epoch (datetime.datetime): When this snakeflake started counting from.
            constants (SnakeflakeConstants): The constants this snakeflake uses.
        """
        return cls(None, None, None, epoch, constants, snakeflake_id,)

    def calculate_snakeflake(self):
        """Calculates a snakeflake.
        
        This method calculates and updates the `snakeflake_id` attribute
        based on the `timestamp`, `serial`, and `machine_id`
        attributes set upon initialization.
        """
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

    def reverse_calculate_snakeflake(self):
        """
        Calculates and updates the snakeflake's attributes from the snakeflake ID.

        Typically used with the :meth:`from_snakeflake` classmethod.
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

    def calculate(self):
        """A generic "smart" calculation method that runs either
        :meth:`calculate_snakeflake` or :meth:`reverse_calculate_snakeflake`
        depending on the current attributes set."""
        if self.snakeflake_id == None:
            self.calculate_snakeflake()
        else:
            self.reverse_calculate_snakeflake()

    def get_id(self):
        """
        Returns:
            int: The snakeflake ID
        """
        return self.snakeflake_id
