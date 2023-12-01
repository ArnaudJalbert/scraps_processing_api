import unittest
from database_director import Director, DEFAULT_DATABASE_TEST, DEFAULT_DATABASE
from pymongo.database import Database


class MyTestCase(unittest.TestCase):
    def test_testing_database_connection(self):
        db = Director().create_database(DEFAULT_DATABASE_TEST)

    def test_real_database_connection(self):
        db = Director().create_database(DEFAULT_DATABASE)

    def test_scraps_collection(self):
        db = Director().create_database(DEFAULT_DATABASE_TEST)
        collection = db.get_collection("scraps")
        self.assertTrue(len(list(collection.find())) > 0)


if __name__ == "__main__":
    unittest.main()
