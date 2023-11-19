import math
import matplotlib.pyplot as plt
import numpy as np
import random
import scipy

DEFAULT_POINTS_AMOUNT: int = 35
RANDOM_DATA_INTERVAL: dict[str, float] = {"start": -10.0, "stop": 10.0}
DEFAULT_Y: float = 0.0

DEFAULT_X_Z_DISTANCE_RANGE: dict[str, float] = {"start": 2.5, "stop": 3.0}
DEFAULT_Y_DISTANCE_RANGE: dict[str, float] = {"start": -0.1, "stop": 0.1}

DEFAULT_THETA_RANGE: dict[str, float] = {"start": 0, "stop": 2 * math.pi}


class RandomDataPointsGenerator:
    points_amount: int = None
    angle: float = None
    _points: np.ndarray = None
    _starting_x: np.array = None
    _starting_y: np.array = None
    _starting_z: np.array = None
    _points_origin: np.array = None
    _random_transformation: bool = None
    _points_generated: bool = False

    def __init__(
        self, points_amount=DEFAULT_POINTS_AMOUNT, random_transformation=True
    ) -> None:
        self.points_amount = points_amount
        # here we can assume that the points are ordered in the way they were captured
        self._points = np.empty(points_amount, dtype=np.ndarray)
        self.angle = 2 * float(math.pi) / float(self.points_amount)
        self._random_transformation = random_transformation

    @property
    def points(self) -> np.ndarray[np.array]:
        """
        Randomly generated points from a points amounts.
        Returns:
            np.ndarray: Multidimensional array of 3D points that mimics the outline of a textile shape
        """
        if not self._points_generated:
            self._generate()
            if self._random_transformation:
                self._make_random_transformation()
            self._points_generated = True
        return self._points

    @property
    def points_origin(self) -> np.array:
        """
        Returns the origin from which the points were created.
        Returns:
            np.array: The origin of the points.
        """
        if self._points_origin is None:
            self._points_origin = np.array(
                [self.starting_x, self.starting_y, self.starting_z]
            )
        return self._points_origin

    @property
    def starting_x(self) -> float:
        """
        Sets the x origin from where the points will be generated
        Returns:
            float: x position of the point origin
        """
        if self._starting_x is None:
            self._starting_x = random.uniform(
                RANDOM_DATA_INTERVAL["start"], RANDOM_DATA_INTERVAL["stop"]
            )

        return self._starting_x

    @property
    def starting_y(self) -> float:
        """
        Sets the y origin from where the points will be generated
        Returns:
            float: y position of the point origin
        """
        if self._starting_y is None:
            self._starting_y = DEFAULT_Y

        return self._starting_y

    @property
    def starting_z(self) -> float:
        """
        Sets the z origin from where the points will be generated
        Returns:
            float: z position of the point origin
        """
        if self._starting_z is None:
            self._starting_z = random.uniform(
                RANDOM_DATA_INTERVAL["start"], RANDOM_DATA_INTERVAL["stop"]
            )

        return self._starting_z

    def _generate(self) -> None:
        """
        Generates random 3D points to mimic the capturing of a 2D shape in a 3D environment.
        The way they are dispersed will depend on the amounts of points that need to be generated.
        """
        for index in range(self.points_amount):
            self._points[index] = self._point_from_origin(index)

    def _point_from_origin(self, index: int) -> np.array:
        """
        Creates a point from the origin depending on the index, points amount and the angle.
        Args:
            index: Current index from which to create the point to.

        Returns:
            np.array: A point computed from the angle, index and points amount.
        """
        distance = random.uniform(
            DEFAULT_X_Z_DISTANCE_RANGE["start"], DEFAULT_X_Z_DISTANCE_RANGE["stop"]
        )
        y_distance = random.uniform(
            DEFAULT_Y_DISTANCE_RANGE["start"], DEFAULT_Y_DISTANCE_RANGE["stop"]
        )
        x = self.starting_x + distance * np.cos(float(index) * self.angle)
        z = self.starting_z + distance * np.sin(float(index) * self.angle)
        y = self.starting_y + y_distance
        return np.array([x, y, z], dtype=float)

    def _make_random_transformation(self) -> None:
        """
        Rotate all points around the current point origin in a random manner.
        """
        theta = random.uniform(
            DEFAULT_THETA_RANGE["start"], DEFAULT_THETA_RANGE["stop"]
        )
        for index, point in enumerate(self._points):
            self._points[index] = self._rotate_point(point, self.points_origin, theta)

    @staticmethod
    def _rotate_point(target_point: np.array, axis: np.array, theta: float) -> np.array:
        """
        Rotates a target point around an axis given a radian(theta).
        Algorithms taken here: https://stackoverflow.com/questions/6802577/rotation-of-3d-vector
        Args:
            target_point: The point to be rotated.
            axis: The axis from which the point will be rotated.
            theta: The angle at which the point will be rotated.

        Returns:
            np.array: The rotated point.
        """
        rotation_matrix = scipy.linalg.expm(
            np.cross(np.eye(3), axis / scipy.linalg.norm(axis) * theta)
        )
        rotate_point = np.dot(rotation_matrix, target_point)
        return rotate_point

    def plot(self) -> None:
        """
        Plots the points in a 3D environment
        """
        x, y, z = zip(*self.points)
        figure = plt.figure()
        axe = figure.add_subplot(111, projection="3d")
        axe.scatter(x, y, z, c="b", marker="o")
        axe.set_xlabel("X Label")
        axe.set_ylabel("Y Label")
        axe.set_zlabel("Z Label")
        axe.set_ylim(0, 1)
        axe.set_title("3D Scatter Plot")
        plt.show()


if __name__ == "__main__":
    random_points_generator = RandomDataPointsGenerator(random_transformation=False)
    random_points_generator.plot()
