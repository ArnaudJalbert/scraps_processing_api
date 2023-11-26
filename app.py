import logging
import os
import sys

from bson.json_util import dumps
from bson.errors import InvalidId
from bson.objectid import ObjectId
from constants import SCRAPS_COLLECTION, EMPTY_DATA, USER_COLLECTION
from business.create_scrap_entity import CreateScrapEntity
from business.create_scrap_record import CreateScrapRecord
from business.create_user_entity import CreateUserEntity
from business.create_user_record import CreateUserRecord
from database_director import Director, DEFAULT_DATABASE_TEST
from exceptions.scrap_exceptions import ScrapException
from exceptions.user_exceptions import UserException
from flask import Flask, render_template, request

logging.basicConfig(level=logging.CRITICAL)


def test_mode():
    return len(sys.argv) > 1 and sys.argv[1] == "test"


def create_app():
    return Flask(__name__)


app = create_app()
if test_mode():
    database = Director().create_database(DEFAULT_DATABASE_TEST)
else:
    database = Director().create_database()


@app.route("/")
def index():
    return render_template("index.html"), 200


@app.get("/scraps")
def get_scraps():
    """
    Retrieves all the available scraps.
    Returns:
        str: JSON formatted string with the scraps' data.
    """
    scraps = list(database.get_collection(SCRAPS_COLLECTION).find())
    return dumps(scraps, indent=2), 200


@app.get("/scraps/<_id>")
def get_scrap_by_id(_id):
    """
    Retrieves a scrap that matches the id provided, if it exists
    Args:
        _id: id of the scraps database entry.

    Returns:
        str: JSON formatted string with the scrap data with corresponding id.
    """
    try:
        scrap = list(
            database.get_collection(SCRAPS_COLLECTION).find({"_id": ObjectId(_id)})
        )
    except InvalidId:
        return EMPTY_DATA, 204

    return dumps(scrap), 200


@app.put("/scraps")
def create_scrap():
    """
    Creates a new scrap.
    Template for the PUT request: scraps_processing_url/scraps?textile-class=textile_class&textile-type=textile_type&color=color&owner=owner&geolocation=geolocation&note=note&dimensions=[dimension]
    Returns:
        str: JSON formatted with all the information of the created scrap.
    """
    # get the data from the url request
    scrap_data = dict(request.args)
    try:
        scrap_entity = CreateScrapEntity(scrap_data, database=database).scrap_entity
    except ScrapException as exception:
        return str(exception), 400

    scrap_record = CreateScrapRecord(scrap_entity, database).create_scrap_record()

    return "Done", 200


@app.post("/scraps/<scrap_id>")
def update_scrap(scrap_id):
    """
    Updates an existing scrap.
    Returns:
        str: JSON formatted string with all the information of the updated scrap.
    """
    # TODO: Use the url query parameters to create a new scrap
    url_args = request.args


@app.post("/create-user")
def create_user():
    # get the data from the url request
    user_data = dict(request.args)

    try:
        user_entity = CreateUserEntity(user_data, database).user_entity
    except UserException as exception:
        return str(exception), 400

    user_record = CreateUserRecord(user_entity, database).create_user_record()

    return "User Created Successfully!", 200


@app.get("/user/<username>")
def get_user_by_name(username):
    """
    Retrieves a user with their name.
    Args:
        username: Name of the user to be retrieved.

    Returns:
        str: JSON formatted string with the scrap data with corresponding id.
    """
    try:
        user = list(
            database.get_collection(USER_COLLECTION).find({"username": username})
        )
    except InvalidId:
        return EMPTY_DATA, 204

    return dumps(user), 200


@app.route("/upload", methods=["POST"])
def upload():
    if "file" not in request.files:
        return "No file part", 400

    file = request.files["file"]
    if file.filename == "":
        return "No selected file", 400

    if file:
        file.save(
            os.path.join(".", "data", "scrap_images", file.filename)
        )  # save the received image
        return f"Stored {file.filename}", 200


if __name__ == "__main__":
    app.run(debug=True, host="192.168.0.10")
