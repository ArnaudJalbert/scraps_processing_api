import numpy as np


class PointsManager:
    _points: list[np.array] = None
    _shape_width: float = None
    _shape_height: float = None

    def __init__(self, points):
        self._points = points

    def _get_max_min_position(self, coord) -> tuple:
        xs = [point[coord] for point in self._points]
        return max(xs), min(xs)

    def _get_shape_center(self) -> np.array:
        max_x, min_x = self._get_max_min_position(0)
        max_y, min_y = self._get_max_min_position(1)
        max_z, min_z = self._get_max_min_position(2)
        middle_x = min_x + ((max_x - min_x) / 2)
        middle_y = min_y + ((max_y - min_y) / 2)
        middle_z = min_z + ((max_z - min_z) / 2)

        return np.array([middle_x, middle_y, middle_z])

    def get_shape_width(self):
        max_x, min_x = self._get_max_min_position(0)
        return max_x - min_x

    def get_shape_height(self):
        max_z, min_z = self._get_max_min_position(2)
        return max_z - min_z

    def get_offset_points(self):
        shape_center = self._get_shape_center()
        new_points = []
        for index, point in enumerate(self._points):
            new_points.append(point - shape_center)

        return new_points
