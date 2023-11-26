import uuid

import requests

from database_director import Director, USERS_COLLECTION
from entities.user import User
from exceptions.user_exceptions import (
    MissingUsername,
    UsernameAlreadyUsed,
    MissingEmail,
    EmailAlreadyUsed,
    MissingPassword,
    InstagramAlreadyUsed,
    MissingInstagram,
    NotAnInstagramAccount,
)
from pymongo.database import Database


class CreateUserEntity:
    def __init__(self, user_data: dict, database: Database = None):
        """
        Args:
            user_data: The dict that contains all the information.
            database: Access to the database.
        """
        self._user_data = user_data
        # initialize the database if not passed
        if database is None:
            self._database = Director().create_database()
        else:
            self._database = database

    def _get_username(self):
        # check that the username key is present
        if "username" not in self._user_data.keys():
            raise MissingUsername()

        username = self._user_data["username"]

        # check if the username already exists
        username_exists = list(
            self._database.get_collection(USERS_COLLECTION).find({"username": username})
        )
        if username_exists:
            raise UsernameAlreadyUsed()

        return username

    def _get_unique_id(self):
        start = 0
        stop = 3
        unique_id = self._user_data["username"][start:stop]

        while True:
            # check if the username already exists
            unique_id_exists = list(
                self._database.get_collection(USERS_COLLECTION).find({"id": unique_id})
            )
            if not unique_id_exists:
                break

            start += 1
            stop += 1

            if stop < len(self._user_data["username"]):
                unique_id = self._user_data["username"][start:stop]
            else:
                unique_id = str(uuid.uuid1())[0:3]

        return unique_id

    def _get_email(self):
        if "email" not in self._user_data.keys():
            raise MissingEmail()

        email = self._user_data["email"]

        # check if the username already exists
        email_exists = list(
            self._database.get_collection(USERS_COLLECTION).find({"email": email})
        )
        if email_exists:
            raise EmailAlreadyUsed()

        return email

    def _get_password(self):
        if "password" not in self._user_data.keys():
            raise MissingPassword()

        password = self._user_data["password"]

        return password

    @staticmethod
    def _is_ig_account(instagram):
        return (
            requests.get(f"https://instagram.com/{instagram}/?_a=1").status_code == 200
        )

    def _get_instagram_handle(self):
        if "instagram" not in self._user_data.keys():
            raise MissingInstagram()

        instagram = self._user_data["instagram"]

        # check if the username already exists
        instagram_exists = list(
            self._database.get_collection(USERS_COLLECTION).find(
                {"instagram": instagram}
            )
        )
        if instagram_exists:
            raise InstagramAlreadyUsed()

        if not self._is_ig_account(instagram):
            raise NotAnInstagramAccount()

        return instagram

    @property
    def user_entity(self) -> User:
        username = self._get_username()
        unique_id = self._get_unique_id()
        email = self._get_email()
        password = self._get_password()
        instagram_handle = self._get_instagram_handle()
        return User(
            user_id=unique_id,
            username=username,
            email=email,
            password=password,
            instagram=instagram_handle,
        )
