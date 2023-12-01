from database_director import Director, USERS_COLLECTION
from entities.user import User
from pymongo.results import InsertOneResult
from pymongo.database import Database


class CreateUserRecord:
    _database: Database = None
    _user: User = None
    _request: dict = None
    _record = None

    def __init__(self, user: User, database: Database = None) -> None:
        self._user = user
        if database is None:
            self._database = Director().create_database()
        else:
            self._database = database

    @property
    def user_request(self) -> dict:
        if self._request is None:
            self._request = dict()
            self._request["user_id"] = self._user.user_id
            self._request["username"] = self._user.username
            self._request["email"] = self._user.email
            self._request["instagram"] = self._user.instagram
            if self._user.password:
                self._request["password"] = self._user.password
            if self._user.description:
                self._request["description"] = self._user.description
            if self._user.scraps:
                self._request["scraps"] = list(self._user.scraps)
        return self._request

    def create_user_record(self) -> InsertOneResult:
        self._record: InsertOneResult = self._database.get_collection(
            USERS_COLLECTION
        ).insert_one(self.user_request)
        return self._record
