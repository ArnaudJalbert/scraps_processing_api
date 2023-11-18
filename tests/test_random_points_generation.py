import unittest

import numpy as np

from random_data_points_generator import (
    RandomDataPointsGenerator,
    DEFAULT_POINTS_AMOUNT,
    RANDOM_DATA_INTERVAL,
)


class TestRandomPointsGeneration(unittest.TestCase):
    def setUp(self) -> None:
        self.random_points_generator = RandomDataPointsGenerator()

    def test_amount_of_points(self):
        self.assertEqual(
            self.random_points_generator.points_amount, DEFAULT_POINTS_AMOUNT
        )

    def test_starting_x(self):
        self.assertTrue(
            RANDOM_DATA_INTERVAL["start"]
            <= self.random_points_generator.starting_x
            <= RANDOM_DATA_INTERVAL["stop"]
        )

    def test_starting_z(self):
        self.assertTrue(
            RANDOM_DATA_INTERVAL["start"]
            <= self.random_points_generator.starting_z
            <= RANDOM_DATA_INTERVAL["stop"]
        )

    def test_starting_y(self):
        self.assertAlmostEqual(self.random_points_generator.starting_y, 0.0)


if __name__ == "__main__":
    unittest.main()
