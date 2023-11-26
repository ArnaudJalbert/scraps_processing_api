import ast
import os.path

import numpy as np

from colour import Color
from database_director import Director
from entities.scrap import Scrap
from exceptions.scrap_exceptions import (
    MissingTextileClass,
    InvalidTextileClass,
    MissingTextileColor,
    MissingTextileDimensions,
    MissingScrapOwner,
    MissingImage,
)
from business.get_textile_classes import get_textile_classes
from business.get_textile_types import get_textile_types
from business.offset_points import PointsManager
from pymongo.database import Database

IMAGE_PATH = "./data/scrap_images/{image_name}.png"


class CreateScrapEntity:
    """This class is used to create a Scrap python entity from raw string data.

    Passing a dictionary where data are all strings, the class will convert all those into the appropriate data types
    to create the Scrap entity.

    It will check to make sure that all data types are valid and fit them properly in the Scrap entity.
    """

    _scrap_data: dict = None
    _database: Database = None
    _scrap_entity: Scrap = None
    _points_manager: PointsManager = None

    def __init__(self, scrap_data: dict, database: Database = None) -> None:
        """
        Args:
            scrap_data: The dict that contains all the information.
            database: Access to the database.
        """
        self._scrap_data = scrap_data
        # initialize the database if not passed
        if database is None:
            self._database = Director().create_database()
        else:
            self._database = database
        # get the textile types and classes
        self._all_textile_classes = get_textile_classes(self._database)
        self._all_textile_types = get_textile_types(self._database)

    def _get_textile_class(self) -> str:
        """
        Check that the textile class is included in the request and that it's a valid one.
        Returns:
            str: The textile class.
        Raises:
            MissingTextileClass: When the textile class is missing.
            InvalidTextileClass: When the textile class is not valid.
        """
        if "textile-class" not in self._scrap_data.keys():
            raise MissingTextileClass()
        if self._scrap_data["textile-class"] not in self._all_textile_classes:
            raise InvalidTextileClass()
        return self._scrap_data["textile-class"]

    def _get_textile_type(self) -> str:
        """
        Check that the textile type is included in the request and that it's a valid one.
        If the textile type is not included, it is assumed that it is "unknown".
        Returns:
            str: The textile type.
        Raises:
            InvalidTextileType: When the textile type is not valid.
        """
        if "textile-type" not in self._scrap_data.keys():
            return "unknown"
        if self._scrap_data["textile-type"] not in self._all_textile_types:
            raise InvalidTextileClass()
        return self._scrap_data["textile-type"]

    def _get_color(self) -> Color:
        """
        Check of the color is included and formats it correctly.
        Returns:
            Color: The color of the textile.
        Raises:
            MissingTextileColor: When the color is not included.
        """
        if "color" not in self._scrap_data.keys():
            raise MissingTextileColor()
        if not self._scrap_data["color"].startswith("#"):
            return Color("#{color}".format(color=self._scrap_data["color"]))
        else:
            return Color(str(self._scrap_data["color"]))

    def _get_owner(self) -> str:
        """
        Check if the owner is included
        Returns:
            str: The owner of the scrap.
        """
        if "owner" not in self._scrap_data.keys():
            raise MissingScrapOwner()
        return self._scrap_data["owner"]

    def _get_geolocation(self) -> [tuple[float, float], None]:
        """
        Check of the geolocation is included and converts it to the correct format.
        Returns:
            None: If the geolocation is not included
            tuple[float, float]: Coordinates of the location
        """
        if "geolocation" not in self._scrap_data.keys():
            return None
        geolocation = tuple(self._scrap_data["geolocation"][1:-1].split(","))
        geolocation = tuple(
            float(geolocation_point) for geolocation_point in geolocation
        )
        print(geolocation)
        return geolocation

    def _get_note(self) -> str:
        """
        Check if the note is included.
        If not, it returns an empty string.
        If it included, returns the note content
        Returns:
            str: The note content.
        """
        if "note" not in self._scrap_data.keys():
            return ""
        return self._scrap_data["note"]

    def _get_dimensions(self) -> list[np.array]:
        """
        Checks if the dimensions are included and convert them into the correct format.
        Returns:
            list[np.array]: The dimensions of the scrap.
        """
        if "dimensions" not in self._scrap_data.keys():
            raise MissingTextileDimensions()
        dimensions = ast.literal_eval(self._scrap_data["dimensions"])
        dimensions = [np.array(coordinate) for coordinate in dimensions]
        self._points_manager = PointsManager(dimensions)
        dimensions = self._points_manager.get_offset_points()
        return dimensions

    def _get_width(self) -> float:
        """
        Returns the width of the shape.
        Returns:
            float: The width of the scrap.
        """
        if self._points_manager is None:
            raise MissingTextileDimensions()
        return self._points_manager.get_shape_width()

    def _get_height(self) -> float:
        """
        Returns the height of the shape.
        Returns:
            float: The height of the scrap.
        """
        if self._points_manager is None:
            raise MissingTextileDimensions()
        return self._points_manager.get_shape_height()

    def _get_image_path(self) -> str:
        """
        Checks if image exists and links the patht.
        Returns:
            str: The path to the image
        """
        if "image" not in self._scrap_data.keys():
            raise MissingImage()

        image_name = self._scrap_data["image"]
        image_path = IMAGE_PATH.format(image_name=image_name)
        if not os.path.exists(image_path):
            raise FileExistsError("The image does not exists.")
        return image_path

    @property
    def scrap_entity(self) -> Scrap:
        """
        Extracts the information of the requests and format them correctly.
        Create the Scrap entity objects from the information.
        Returns:
            Scrap: The scrap information in the entity.
        """
        if self._scrap_entity is not None:
            return self._scrap_entity

        # change all %20 to spaces
        for key, value in self._scrap_data.items():
            self._scrap_data[key] = str(value).replace("%20", " ")

        textile_class = self._get_textile_class()
        textile_type = self._get_textile_type()
        color = self._get_color()
        owner = self._get_owner()
        geolocation = self._get_geolocation()
        note = self._get_note()
        dimensions = self._get_dimensions()
        width = self._get_width()
        height = self._get_height()
        image = self._get_image_path()

        return Scrap(
            fabric_class=textile_class,
            fabric_type=textile_type,
            color=color,
            owner=owner,
            geolocation=geolocation,
            note=note,
            dimensions=dimensions,
            image_path=image,
            width=width,
            height=height,
        )
