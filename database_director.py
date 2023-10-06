import logging
import pymongo
import os

from dotenv import load_dotenv

# load env var into memory
load_dotenv()


class Director:
    _databases = dict()
    _mongo_client = None
    _LOG = None

    def __init__(self):
        self._LOG = logging.getLogger(self.__class__.__name__)

    @property
    def mongo_client(self):
        """
        Creates a connection to the Mongo client
        Returns:
            MongoClient: A Mongo client connection
        """
        if self._mongo_client is None:
            self._LOG.info("Connecting to the MongoDB client.")
            self._mongo_client = pymongo.MongoClient(os.environ.get("MONGO_URI"))
            return self._mongo_client
        else:
            return self._mongo_client

    def create_database(self, database_name="scraps_processing"):
        """
        Creates a mongo database instance given a database name
        Args:
            database_name(str): The name of the database.

        Returns:
            Database: A PyMongo database with associated name.
        """
        if database_name in self._databases:
            return self._databases[database_name]
        else:
            self._LOG.info(f"Trying to load database '{database_name}'.")
            database = self.mongo_client.get_database(database_name)
            self._LOG.info(f"Loaded database '{database.name}' successfully.")
            self._databases[database_name] = database
            return database
