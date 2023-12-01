from database_director import TEXTILE_TYPES_COLLECTION
from pymongo.database import Database


def get_textile_types(database: Database):
    textile_classes_response = list(
        database.get_collection(TEXTILE_TYPES_COLLECTION).find()
    )
    return {response["textile_type"] for response in textile_classes_response}
