import unittest
from random_data_points_generator import (
    RandomDataPointsGenerator,
    DEFAULT_POINTS_AMOUNT,
    RANDOM_DATA_INTERVAL,
    DEFAULT_X_Y_DISTANCE_RANGE,
    DEFAULT_Z_DISTANCE_RANGE,
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

    def test_starting_y(self):
        self.assertTrue(
            RANDOM_DATA_INTERVAL["start"]
            <= self.random_points_generator.starting_y
            <= RANDOM_DATA_INTERVAL["stop"]
        )

    def test_starting_z(self):
        self.assertAlmostEqual(self.random_points_generator.starting_z, 0.0)

    def test_points_assignment(self):
        self.random_points_generator.generate()

    def test_z_points(self):
        self.random_points_generator.generate()
        for point in self.random_points_generator.points:
            self.assertTrue(
                DEFAULT_Z_DISTANCE_RANGE["start"]
                <= point[2]
                <= DEFAULT_Z_DISTANCE_RANGE["stop"]
            )

    def test_x_points(self):
        self.random_points_generator.generate()
        for point in self.random_points_generator.points:
            self.assertTrue(
                DEFAULT_X_Y_DISTANCE_RANGE["start"]
                <= (self.random_points_generator.starting_x - point[0])
                <= DEFAULT_X_Y_DISTANCE_RANGE["stop"]
            )


if __name__ == "__main__":
    unittest.main()
