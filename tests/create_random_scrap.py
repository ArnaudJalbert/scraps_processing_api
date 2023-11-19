import numpy as np
import random

from colour import Color
from database_director import Director, DEFAULT_DATABASE_TEST
from entities.scrap import Scrap
from tests.random_data_points_generator import RandomDataPointsGenerator


class CreateTestScraps:
    scraps = list()
    scraps_amount = 0
    _textile_classes = None
    _textile_types = None
    _database = None

    def __init__(self, scraps_amount=0):
        self.scraps_amount = scraps_amount

    @property
    def database(self):
        if self._database is None:
            self._database = Director().create_database(DEFAULT_DATABASE_TEST)
        return self._database

    @property
    def textile_classes(self):
        if self._textile_classes is None:
            self._textile_classes = list(
                self.database.get_collection("textile_classes").find()
            )
        return self._textile_classes

    @property
    def textile_types(self):
        if self._textile_types is None:
            self._textile_types = list(
                self.database.get_collection("textile_types").find()
            )
        return self._textile_types

    @staticmethod
    def generate_random_color():
        return "#%06x" % random.randint(0, 0xFFFFF)

    @staticmethod
    def generate_random_points():
        ramdom_points = RandomDataPointsGenerator(
            points_amount=5, random_transformation=False
        ).points
        x_z_points = list()
        for point in ramdom_points:
            x_z_points.append(np.array([point[0], point[1]]))
        return x_z_points

    def random_textile_class(self):
        return random.choice(self.textile_classes)["textile_class"]

    def random_textile_type(self, textile_class):
        while True:
            textile_type = random.choice(self.textile_types)
            if textile_type["textile_class"] == textile_class:
                return textile_type["textile_type"]

    def create_scraps(self):
        for index in range(self.scraps_amount):
            textile_class = self.random_textile_class()
            textile_type = self.random_textile_type(textile_class)
            random_points = self.generate_random_points()
            scrap = Scrap(
                id=0,
                color=Color(self.generate_random_color()),
                fabric_class=textile_class,
                dimensions=random_points,
                owner="Arnaud Jalbert",
                fabric_type=textile_type,
                note="Test Note!",
            )
            self.scraps.append(scrap)


if __name__ == "__main__":
    test_scraps = CreateTestScraps(10)
    test_scraps.create_scraps()
    print(test_scraps.scraps)
