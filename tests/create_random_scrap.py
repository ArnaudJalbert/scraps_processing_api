import time

import random

from business.create_scrap_entity import CreateScrapEntity
from business.create_scrap_record import CreateScrapRecord
from database_director import Director, DEFAULT_DATABASE_TEST
from faker import Faker
from tests.random_data_points_generator import RandomDataPointsGenerator

TEST_IMAGE_PATH = "../data/scrap_images/test_image.jpg"


class CreateTestScraps:
    scraps = list()
    scraps_amount = 0
    _textile_classes = None
    _textile_types = None
    _database = None
    _fake = Faker()

    def __init__(self, scraps_amount=0):
        self.scraps_amount = scraps_amount
        Faker.seed(time.time())

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
        return "%06x" % random.randint(0, 0xFFFFF)

    @staticmethod
    def generate_random_points():
        ramdom_points = RandomDataPointsGenerator(
            points_amount=5, random_transformation=False
        ).points
        ramdom_points = (
            str(ramdom_points)
            .replace("array", "")
            .replace(" dtype=object", "")
            .replace("(", "")
            .replace(")", "")
            .replace("\n", ",")
        )
        return ramdom_points

    def random_textile_class(self):
        return random.choice(self.textile_classes)["textile_class"]

    def random_textile_type(self, textile_class):
        while True:
            textile_type = random.choice(self.textile_types)
            if textile_type["textile_class"] == textile_class:
                return textile_type["textile_type"]

    def random_geolocation(self):
        coordinates = self._fake.local_latlng(country_code="CA")
        return f"[{coordinates[0]},{coordinates[1]}]"

    def create_scraps(self):
        for index in range(self.scraps_amount):
            args = dict()
            args["textile-class"] = self.random_textile_class()
            args["textile-type"] = self.random_textile_type(args["textile-class"])
            args["random_points"] = self.generate_random_points()
            args["color"] = self.generate_random_color()
            args["owner"] = "arn"
            args["geolocation"] = self.random_geolocation()
            args["note"] = "Test Notes"
            args["dimensions"] = self.generate_random_points()
            args["image"] = "test_image"

            scrap_entity = CreateScrapEntity(
                args, self.database, ignore_image=True
            ).scrap_entity
            CreateScrapRecord(scrap_entity, self.database).create_scrap_record()
            time.sleep(0.1)


if __name__ == "__main__":
    create_test_scraps = CreateTestScraps(5)
    create_test_scraps.create_scraps()
