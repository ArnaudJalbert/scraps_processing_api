import ast
import numpy as np

from colour import Color
from database_director import Director
from entities.scrap import Scrap
from exceptions.scrap_exceptions import (
    MissingTextileClass,
    InvalidTextileClass,
    MissingTextileColor,
    MissingTextileDimensions,
)
from business.get_textile_classes import get_textile_classes
from business.get_textile_types import get_textile_types
from pymongo.database import Database


class CreateScrapEntity:
    """This class is used to create a Scrap python entity from raw string data.

    Passing a dictionary where data are all strings, the class will convert all those into the appropriate data types
    to create the Scrap entity.

    It will check to make sure that all data types are valid and fit them properly in the Scrap entity.
    """

    _scrap_data: dict = None
    _database: Database = None
    _scrap_entity: Scrap = None

    def __init__(self, scrap_data: dict, database: Database = None):
        """

        Args:
            scrap_data: The dict that contains all the information
            database:
        """
        self._scrap_data = scrap_data
        if database is None:
            self._database = Director().create_database()
        else:
            self._database = database
        self._all_textile_classes = get_textile_classes(self._database)
        self._all_textile_types = get_textile_types(self._database)

    def _get_textile_class(self):
        if "textile-class" not in self._scrap_data.keys():
            raise MissingTextileClass()
        if self._scrap_data["textile-class"] not in self._all_textile_classes:
            raise InvalidTextileClass()
        return self._scrap_data["textile-class"]

    def _get_textile_type(self):
        if "textile-type" not in self._scrap_data.keys():
            return "unknown"
        if self._scrap_data["textile-type"] not in self._all_textile_types:
            raise InvalidTextileClass()
        return self._scrap_data["textile-type"]

    def _get_color(self):
        if "color" not in self._scrap_data.keys():
            raise MissingTextileColor()
        if not self._scrap_data["color"].startswith("#"):
            return Color("#{color}".format(color=self._scrap_data["color"]))
        else:
            return Color(str(self._scrap_data["color"]))

    def _get_owner(self):
        return self._scrap_data["owner"]

    def _get_geolocation(self):
        if "geolocation" not in self._scrap_data.keys():
            return None
        geolocation = tuple(self._scrap_data["geolocation"][1:-1].split(","))
        return geolocation

    def _get_note(self):
        if "note" not in self._scrap_data.keys():
            return ""
        return self._scrap_data["note"]

    def _get_dimensions(self):
        if "dimensions" not in self._scrap_data.keys():
            raise MissingTextileDimensions()
        dimensions = ast.literal_eval(self._scrap_data["dimensions"])
        dimensions = [np.array(coordinate) for coordinate in dimensions]
        return dimensions

    @property
    def scrap_entity(self):
        if self._scrap_entity is not None:
            return self._scrap_entity

        textile_class = self._get_textile_class()
        textile_type = self._get_textile_type()
        color = self._get_color()
        owner = self._get_owner()
        geolocation = self._get_geolocation()
        note = self._get_note()
        dimensions = self._get_dimensions()

        return Scrap(
            id="unknown",
            fabric_class=textile_class,
            fabric_type=textile_type,
            color=color,
            owner=owner,
            geolocation=geolocation,
            note=note,
            dimensions=dimensions,
        )
