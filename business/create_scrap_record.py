from database_director import Director
from entities.scrap import Scrap
from pymongo.database import Database


class CreateScrapRecord:
    _database: Database = None
    _scrap: Scrap = None

    def __init__(self, scrap: Scrap, database: Database = None):
        if database is None:
            self._database = Director().create_database()
        else:
            self._database = database
        self._scrap = scrap

    def _get_dimensions_list(self):
        dimensions = list()
        for dimension in self._scrap.dimensions:
            dimensions.append([dimension[0], dimension[1]])
        return dimensions

    def _create_scrap_dict(self):
        scrap_dict = dict()

        scrap_dict["color"] = self._scrap.color.hex
        scrap_dict["fabric_class"] = self._scrap.fabric_class
        scrap_dict["dimensions"] = self._get_dimensions_list()
        scrap_dict["owner"] = self._scrap.owner
        if self._scrap.geolocation:
            scrap_dict["geolocation"] = self._scrap.geolocation
        if self._scrap.fabric_type:
            scrap_dict["fabric_type"] = self._scrap.fabric_type
        if self._scrap.note:
            scrap_dict["note"] = self._scrap.note

        return scrap_dict

    def execute(self):
        record_dict = self._create_scrap_dict()
        self._database.get_collection("scraps").insert_one(record_dict)
