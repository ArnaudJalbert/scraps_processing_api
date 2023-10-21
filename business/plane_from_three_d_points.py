import numpy as np

from typing import List


class PlaneFromThreeDPoints:
    points = None

    def __init__(self, three_d_points: List[np.ndarray]) -> None:
        """

        Args:
            three_d_points: 3D points sampled from the outline of the object
        """
        self.points = three_d_points
