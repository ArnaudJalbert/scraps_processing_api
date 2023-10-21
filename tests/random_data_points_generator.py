import matplotlib.pyplot as plt
import numpy as np
import random

from mpl_toolkits.mplot3d import Axes3D

DEFAULT_POINTS_AMOUNT = 35
RANDOM_DATA_INTERVAL = {"start": -10.0, "stop": 10.0}
DEFAULT_Z = 0.0

DEFAULT_X_Y_DISTANCE_RANGE = {"start": 2.5, "stop": 3.0}
DEFAULT_Z_DISTANCE_RANGE = {"start": -0.1, "stop": 0.1}


class RandomDataPointsGenerator:
    points_amount = None
    points = None
    angle = None
    _starting_x = None
    _starting_y = None
    _starting_z = None

    def __init__(self, points_amount=DEFAULT_POINTS_AMOUNT) -> None:
        self.points_amount = points_amount
        self.points = np.empty(points_amount, dtype=np.ndarray)
        self.angle = 2 * np.pi / self.points_amount

    def generate(self):
        for index in range(self.points_amount):
            print(self.point_from_origin(index))
            self.points[index] = self.point_from_origin(index)

    def point_from_origin(self, index):
        distance = random.uniform(
            DEFAULT_X_Y_DISTANCE_RANGE["start"], DEFAULT_X_Y_DISTANCE_RANGE["stop"]
        )
        z_distance = random.uniform(
            DEFAULT_Z_DISTANCE_RANGE["start"], DEFAULT_Z_DISTANCE_RANGE["stop"]
        )
        x = self.starting_x + distance * np.cos(float(index) * self.angle)
        y = self.starting_y + distance * np.sin(float(index) * self.angle)
        z = self.starting_z + z_distance
        return np.array([x, y, z], dtype=float)

    @property
    def starting_x(self):
        if self._starting_x is not None:
            return self._starting_x

        self._starting_x = random.uniform(
            RANDOM_DATA_INTERVAL["start"], RANDOM_DATA_INTERVAL["stop"]
        )
        return self._starting_x

    @property
    def starting_y(self):
        if self._starting_y is not None:
            return self._starting_y

        self._starting_y = random.uniform(
            RANDOM_DATA_INTERVAL["start"], RANDOM_DATA_INTERVAL["stop"]
        )
        return self._starting_y

    @property
    def starting_z(self):
        if self._starting_z is not None:
            return self._starting_z

        self._starting_z = DEFAULT_Z
        return self._starting_z

    def plot(self):
        x, y, z = zip(*self.points)
        figure = plt.figure()
        axe = figure.add_subplot(111, projection="3d")
        axe.scatter(x, y, z, c="b", marker="o")
        axe.set_zlim(-1, 1)
        axe.set_xlabel("X Label")
        axe.set_ylabel("Y Label")
        axe.set_zlabel("Z Label")
        axe.set_title("3D Scatter Plot")
        plt.show()


if __name__ == "__main__":
    random_points_generator = RandomDataPointsGenerator()
    random_points_generator.generate()
    random_points_generator.plot()
