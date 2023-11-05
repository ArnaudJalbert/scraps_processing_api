import matplotlib.pyplot as plt
import numpy as np

from tests.random_data_points_generator import RandomDataPointsGenerator


class PlaneFromThreeDPoints:
    _points: np.ndarray[np.array] = None
    _xs: list = None
    _ys: list = None
    _zs: list = None
    _A: np.matrix = None
    _B: np.matrix = None
    _fit: np.matrix = None
    _errors: np.matrix = None
    _residual: np.float64 = None
    _a: float = None
    _b: float = None
    _c: float = None

    def __init__(self, three_d_points: np.ndarray[np.array]) -> None:
        """
        Args:
            three_d_points: 3D points sampled from the outline of the object
        """
        self._points = three_d_points
        self._xs = [point[0] for point in self._points]
        self._ys = [point[1] for point in self._points]
        self._zs = [point[2] for point in self._points]

    @property
    def a(self):
        """
        Sets "a" parameter of the plane equation
        Returns:
            float: a parameter of the plane equation
        """
        if self._a is None:
            self._fit_points()
        return self._a

    @property
    def b(self):
        """
        Sets "b" parameter of the plane equation
        Returns:
            float: b parameter of the plane equation
        """
        if self._b is None:
            self._fit_points()
        return self._b

    @property
    def c(self):
        """
        Sets "b" parameter of the plane equation
        Returns:
            float: b parameter of the plane equation
        """
        if self._c is None:
            self._fit_points()
        return self._c

    def _fit_points(self):
        """
        Approximates an equation of a plane from the set of 3D points.
        Source:
        https://brilliant.org/wiki/3d-coordinate-geometry-equation-of-a-plane/
        https://stackoverflow.com/questions/20699821/find-and-draw-regression-plane-to-a-set-of-points
        """
        # temporary containers to separate the x and y values from the z values
        tmp_A = np.empty((len(self._points), 3))
        tmp_b = np.empty(len(self._points))

        for index, point in enumerate(self._points):
            # A contains the x and y points -> [x, y, 1]
            tmp_A[index] = [point[0], point[1], 1]
            # b contains the z points -> [z]
            tmp_b[index] = point[2]
        # create matrices from
        self._A = np.matrix(tmp_A)
        self._B = np.matrix(tmp_b).T

        # [a,b,c] = (A^T * A)^-1 * A^T * B
        self._fit = (self._A.T * self._A).I * self._A.T * self._B
        self._errors = self._B - self._A * self._fit
        self._residual = np.linalg.norm(self._errors)
        self._a = self._fit[0]
        self._b = self._fit[1]
        self._c = self._fit[2]

    def plot(self):
        """
        Plots the plane along the point to see the accuracy.
        """
        plt.figure()
        ax = plt.subplot(111, projection="3d")
        ax.scatter(self._xs, self._ys, self._zs, color="b")
        xlim = ax.get_xlim()
        ylim = ax.get_ylim()
        X, Y = np.meshgrid(np.arange(xlim[0], xlim[1]), np.arange(ylim[0], ylim[1]))
        Z = np.zeros(X.shape)
        for r in range(X.shape[0]):
            for c in range(X.shape[1]):
                Z[r, c] = self.a * X[r, c] + self.b * Y[r, c] + self.c
        ax.plot_wireframe(X, Y, Z, color="k")
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.set_zlabel("z")
        plt.show()


if __name__ == "__main__":
    points = RandomDataPointsGenerator().points
    plane = PlaneFromThreeDPoints(points)
    plane.plot()
