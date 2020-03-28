import unittest
import datetime
import random
from snakeflake import snakeflake, config


class TestSnakeflakeGeneration(unittest.TestCase):
    def test_snakeflake(self):
        epoch = datetime.datetime.utcnow()
        sf_constants = config.SnakeflakeConstants.defaults()

        machine_id = random.randint(0, 2 ** sf_constants.machine_id_bits)

        sf_config = config.SnakeflakeGeneratorConfig(epoch, machine_id, sf_constants)

        sf_gen = snakeflake.SnakeflakeGenerator(sf_config)

        new_snakeflake = sf_gen.next_snakeflake()

        other_snakeflake = snakeflake.Snakeflake.from_snakeflake(
            new_snakeflake.get_id(), epoch, sf_constants
        )
        other_snakeflake.reverse_calculate_snakeflake()

        print(new_snakeflake.snakeflake_id)
        print(other_snakeflake.snakeflake_id)
        # self.assertEqual(new_snakeflake, other_snakeflake)
