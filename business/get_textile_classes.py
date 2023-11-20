from database_director import TEXTILE_CLASSES_COLLECTION
from pymongo.database import Database


def get_textile_classes(database: Database):
    textile_classes_response = list(
        database.get_collection(TEXTILE_CLASSES_COLLECTION).find()
    )
    return {response["textile_class"] for response in textile_classes_response}
