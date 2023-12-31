from database_director import Director, DEFAULT_DATABASE_TEST

NATURAL_TEXTILE_TYPES = [
    "Cotton",
    "Linen",
    "Wool",
    "Silk",
    "Hemp",
    "Jute",
    "Ramie",
    "Alpaca",
    "Angora",
    "Bamboo",
    "Tencel",
]

SYNTHETIC_TEXTILE_TYPES = [
    "Polyester",
    "Nylon",
    "Acrylic",
    "Spandex",
    "Rayon",
    "PVC (Polyvinyl chloride)",
    "Acetate",
    "Polypropylene",
    "Modal",
    "Olefin",
    "Elastane",
]

TEXTILE_CLASSES = ["Synthetic", "Natural"]


def insert_natural_textile_types(database):
    textile_types_collection = database.get_collection("textile_types")
    for textile_type in NATURAL_TEXTILE_TYPES:
        textile_types_collection.insert_one(
            {"textile_type": textile_type.lower(), "textile_class": "natural"}
        )


def insert_synthetic_textile_types(database):
    textile_types_collection = database.get_collection("textile_types")
    for textile_type in SYNTHETIC_TEXTILE_TYPES:
        textile_types_collection.insert_one(
            {"textile_type": textile_type.lower(), "textile_class": "synthetic"}
        )


def insert_textile_classes(database):
    textile_types_collection = database.get_collection("textile_classes")
    for textile_class in TEXTILE_CLASSES:
        textile_types_collection.insert_one({"textile_class": textile_class.lower()})


if __name__ == "__main__":
    db = Director().create_database()
    insert_textile_classes(db)
