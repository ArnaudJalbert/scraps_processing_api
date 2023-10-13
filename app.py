import logging

from bson.json_util import dumps
from bson.errors import InvalidId
from bson.objectid import ObjectId
from constants import SCRAPS_COLLECTION, EMPTY_DATA
from database_director import Director
from flask import Flask, render_template, request

logging.basicConfig(level=logging.CRITICAL)

director = Director()
database = director.create_database()


def create_app():
    return Flask(__name__)


app = create_app()


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
    print(request.args.keys())
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


@app.post("/scraps")
def create_new_scrap():
    """

    Returns:

    """


if __name__ == "__main__":
    app.run(debug=True)
