import cloudinary.uploader
import logging
import os
import sys
import time

from bson.json_util import dumps
from bson.errors import InvalidId
from bson.objectid import ObjectId
from constants import SCRAPS_COLLECTION, EMPTY_DATA, USER_COLLECTION
from business.create_scrap_entity import CreateScrapEntity
from business.create_scrap_record import CreateScrapRecord
from business.create_user_entity import CreateUserEntity
from business.create_user_record import CreateUserRecord
from database_director import (
    Director,
    DEFAULT_DATABASE_TEST,
    TEXTILE_CLASSES_COLLECTION,
    TEXTILE_TYPES_COLLECTION,
)
from exceptions.scrap_exceptions import ScrapException
from exceptions.user_exceptions import UserException
from flask import Flask, render_template, request, send_file
from geopy import distance
from dotenv import load_dotenv

logging.basicConfig(level=logging.CRITICAL)

load_dotenv()


cloudinary.config(
    cloud_name="dm2ernrfn",
    api_key="535384942931621",
    api_secret=os.environ.get("CLOUDINARY_API_KEY"),
)


def test_mode():
    return len(sys.argv) > 1 and sys.argv[1] == "test"


def create_app():
    return Flask(__name__)


app = create_app()
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
    url_args = dict(request.args)
    mongo_filter = dict(url_args)
    # remove distance information
    mongo_filter.pop("distance", None)
    mongo_filter.pop("longitude", None)
    mongo_filter.pop("latitude", None)
    scraps = list(database.get_collection(SCRAPS_COLLECTION).find(mongo_filter))
    # check if distance is filtered
    if "distance" not in url_args.keys():
        return dumps(scraps), 200

    close_scraps = list()
    for scrap in scraps:
        if "geolocation" not in scrap.keys():
            close_scraps.append(scrap)
            continue
        origin = (float(url_args["latitude"]), float(url_args["longitude"]))
        scrap_location = (
            float(scrap["geolocation"][0]),
            float(scrap["geolocation"][1]),
        )
        scrap_distance = distance.distance(origin, scrap_location).km
        print(scrap_distance)
        if scrap_distance < float(url_args["distance"]):
            close_scraps.append(scrap)
    return dumps(close_scraps), 200


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
        # try with scrap id instead
        if not scrap:
            scrap = list(database.get_collection(SCRAPS_COLLECTION).find({"id": _id}))
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
        # create the scrap entity
        scrap_entity = CreateScrapEntity(scrap_data, database=database).scrap_entity
    except ScrapException as exception:
        return str(exception), 400

    scrap_record = CreateScrapRecord(scrap_entity, database).create_scrap_record()

    scrap_data = get_scrap_by_id(scrap_record.inserted_id)

    return scrap_data[0], 200


@app.put("/scraps/<scrap_id>")
def update_scrap(scrap_id):
    """
    Updates an existing scrap.
    Returns:
        str: JSON formatted string with all the information of the updated scrap.
    """
    url_args = dict(request.args)

    scrap = {"id": scrap_id}
    update = {"$set": {url_args["key"]: url_args["value"]}}

    database.get_collection(SCRAPS_COLLECTION).update_one(scrap, update)

    updated_scrap = list(database.get_collection(SCRAPS_COLLECTION).find(scrap))

    return dumps(updated_scrap), 200


@app.get("/scraps/<scrap_id>/image")
def get_scrap_image_by_id(scrap_id):
    """
    Get the current textile types that are available.
    Returns:
        str: json formatted string of all textile classes
    """
    scrap_image = list(
        database.get_collection(SCRAPS_COLLECTION).find({"id": scrap_id})
    )[0]["image_path"]

    image_url = cloudinary.CloudinaryImage(scrap_image).build_url()
    image_url += ".png"

    return dumps(image_url), 200



@app.post("/create-user")
def create_user():
    # get the data from the url request
    user_data = dict(request.args)

    try:
        user_entity = CreateUserEntity(user_data, database).user_entity
    except UserException as exception:
        return str(exception), 400

    response = CreateUserRecord(user_entity, database).create_user_record()

    user = list(
        database.get_collection(USER_COLLECTION).find(
            {"_id": ObjectId(str(response.inserted_id))}
        )
    )

    return dumps(user), 200


@app.get("/user/<username>")
def get_user_by_name(username):
    """
    Retrieves a user with their username, email or instagram.
    Args:
        username: Name, email or instagram of the user to be retrieved.

    Returns:
        str: JSON formatted string with the scrap data with corresponding id.
    """
    try:
        user = list(
            database.get_collection(USER_COLLECTION).find(
                {"username": username.lower()}
            )
        )
        email = list(
            database.get_collection(USER_COLLECTION).find({"email": username.lower()})
        )
        instagram = list(
            database.get_collection(USER_COLLECTION).find(
                {"instagram": username.lower()}
            )
        )
        user_id = list(
            database.get_collection(USER_COLLECTION).find({"user_id": username})
        )
    except InvalidId:
        return EMPTY_DATA, 204
    except Exception as exception:
        return str(exception), 400

    print(instagram)

    if user:
        return dumps(user[0]), 200
    elif email:
        return dumps(email[0]), 200
    elif instagram:
        return dumps(instagram[0]), 200
    elif user_id:
        return dumps(user_id[0]), 200
    else:
        return EMPTY_DATA, 204


@app.get("/user/<username>/user-id")
def get_user_id_by_name(username):
    """
    Retrieves a user with their username, email or instagram.
    Args:
        username: Name, email or instagram of the user to be retrieved.

    Returns:
        str: JSON formatted string with the scrap data with corresponding id.
    """
    try:
        user = list(
            database.get_collection(USER_COLLECTION).find(
                {"username": username.lower()}
            )
        )
        email = list(
            database.get_collection(USER_COLLECTION).find({"email": username.lower()})
        )
        instagram = list(
            database.get_collection(USER_COLLECTION).find(
                {"instagram": username.lower()}
            )
        )
        user_id = list(
            database.get_collection(USER_COLLECTION).find({"user_id": username})
        )
    except InvalidId:
        return EMPTY_DATA, 204

    if user:
        return user[0]["user_id"], 200
    elif email:
        return email[0]["user_id"], 200
    elif instagram:
        return instagram[0]["user_id"], 200
    elif user_id:
        return dumps(user_id[0]["user_id"]), 200
    else:
        return EMPTY_DATA, 204


@app.route("/upload", methods=["POST"])
def upload():
    if "file" not in request.files:
        return "No file part", 400

    file = request.files["file"]
    if file.filename == "":
        return "No selected file", 400

    if file:
        path = os.path.join(".", "data", "scrap_images", file.filename)
        file.save(path)  # save the received image
        while not os.path.exists(path):
            time.sleep(1)
        response = cloudinary.uploader.upload(path, public_id=file.filename.replace(".png", ""))
        print(response)
        return f"Stored {file.filename}", 200


@app.get("/textile-classes")
def get_textile_classes():
    """
    Get the current textile classes that are available.
    Returns:
        str: json formatted string of all textile classes
    """
    try:
        textile_classes_dict = list(
            database.get_collection(TEXTILE_CLASSES_COLLECTION).find(
                {}, {"textile_class": 1, "_id": 0}
            )
        )
    except Exception as exception:
        return str(exception), 204
    textile_classes = list()

    # get only the values not the whole dict
    for textile_class in textile_classes_dict:
        value = textile_class["textile_class"]
        textile_classes.append(value)

    return dumps(textile_classes), 200


@app.get("/textile-types")
def get_textile_types(textile_class=None):
    """
    Get the current textile types that are available.
    Returns:
        str: json formatted string of all textile classes
    """
    try:
        if textile_class:
            textile_filter = {"textile_class": textile_class}
        else:
            textile_filter = {}
        textile_types_dict = list(
            database.get_collection(TEXTILE_TYPES_COLLECTION).find(
                textile_filter, {"textile_type": 1, "_id": 0}
            )
        )
    except Exception as exception:
        return str(exception), 204
    textile_types = list()

    # get only the values not the whole dict
    for textile_type in textile_types_dict:
        value = textile_type["textile_type"]
        textile_types.append(value)

    return dumps(textile_types), 200


@app.get("/textile-types/<textile_class>")
def get_textile_types_by_class(textile_class):
    """
    Get the current textile types that are available.
    Returns:
        str: json formatted string of all textile classes
    """
    return get_textile_types(textile_class)


if __name__ == "__main__":
    app.run(debug=True, host="192.168.0.10")
