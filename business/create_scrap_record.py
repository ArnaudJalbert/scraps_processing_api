from database_director import Director
from entities.scrap import Scrap
from pymongo.results import InsertOneResult
from pymongo.database import Database


class CreateScrapRecord:
    _database: Database = None
    _scrap: Scrap = None
    _request: dict = None
    _record = None

    def __init__(self, scrap: Scrap, database: Database = None) -> None:
        self._scrap = scrap
        if database is None:
            self._database = Director().create_database()
        else:
            self._database = database

    def _get_dimensions_list(self) -> list[list]:
        dimensions = list()
        for dimension in self._scrap.dimensions:
            dimensions.append([float(dimension[0]), float(dimension[2])])
        return dimensions

    @property
    def scrap_request(self):
        if self._request is None:
            self._request = dict()
            self._request["color"] = self._scrap.color.hex
            self._request["fabric_class"] = self._scrap.fabric_class
            self._request["dimensions"] = self._get_dimensions_list()
            self._request["owner"] = self._scrap.owner
            self._request["image_path"] = self._scrap.image_path
            if self._scrap.geolocation:
                self._request["geolocation"] = self._scrap.geolocation
            if self._scrap.fabric_type:
                self._request["fabric_type"] = self._scrap.fabric_type
            if self._scrap.note:
                self._request["note"] = self._scrap.note
            if self._scrap.id:
                self._request["id"] = self._scrap.id

        return self._request

    def create_scrap_record(self) -> InsertOneResult:
        self._record: InsertOneResult = self._database.get_collection(
            "scraps"
        ).insert_one(self.scrap_request)
        return self._record
