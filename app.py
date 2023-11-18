import logging
import sys

from bson.json_util import dumps
from bson.errors import InvalidId
from bson.objectid import ObjectId
from constants import SCRAPS_COLLECTION, EMPTY_DATA, USER_COLLECTION
from database_director import Director, DEFAULT_DATABASE_TEST
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
    Returns:
        str: JSON formatted with all the information of the created scrap.
    """
    # TODO: Use the url query parameters to create a new scrap
    url_args = request.args

    # TODO: Pass all arguments to the

    return "Done", 200


@app.post("/scraps/<id>")
def update_scrap():
    """
    Updates an existing scrap.
    Returns:
        str: JSON formatted string with all the information of the updated scrap.
    """
    # TODO: Use the url query parameters to create a new scrap
    url_args = request.args

    # TODO: Pass all arguments to the


@app.get("/user/<name>")
def get_user_by_name(name):
    """
    Retrieves a user with their name.
    Args:
        name: Name of the user to be retrieved.

    Returns:
        str: JSON formatted string with the scrap data with corresponding id.
    """
    try:
        user = list(database.get_collection(USER_COLLECTION).find({"name": name}))
    except InvalidId:
        return EMPTY_DATA, 204

    return dumps(user), 200


if __name__ == "__main__":
    app.run(debug=True)
