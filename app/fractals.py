"""Fractal CRUD management"""

from pymongo.errors import DuplicateKeyError
from bson import ObjectId


def fractals_add(**request):
    """Add new fractal"""
    body = request["body"]
    print("Adding fractal", body)
    from . import get_mongo  # pylint: disable=import-outside-toplevel
    mongo = get_mongo()
    try:
        saved = mongo.db.fractals.insert_one({
            "complex_real": body["complex_real"],
            "complex_imaginary": body["complex_imaginary"]
        })
    except DuplicateKeyError as err:
        print("Failed to add new fractal:", err)
        return (None, 409)
    print("Added fractal", saved.inserted_id)
    return None



def fractals_update(fractal_id, **request):
    """Update existing fractal"""
    body = request["body"]
    print("Updating fractal", body, "id", fractal_id)
    from . import get_mongo  # pylint: disable=import-outside-toplevel
    mongo = get_mongo()
    try:
        saved = mongo.db.fractals.update_one({"_id": ObjectId(fractal_id)}, {"$set": {
            "complex_real": body["complex_real"],
            "complex_imaginary": body["complex_imaginary"]
        }})
    except DuplicateKeyError as err:
        print("Failed to update fractal:", err)
        return (None, 409)
    print("Updated fractal", fractal_id, "matches", saved.matched_count)
    return None


def fractals_delete(fractal_id):
    """Delete existing fractal"""
    print("Deleting fractal", fractal_id)
    from . import get_mongo  # pylint: disable=import-outside-toplevel
    mongo = get_mongo()
    saved = mongo.db.fractals.delete_one({"_id": ObjectId(fractal_id)})
    print("Delete fractal", fractal_id, "matches", saved.deleted_count)


def fractals_list():
    """List all fractals"""
    from . import get_mongo  # pylint: disable=import-outside-toplevel
    mongo = get_mongo()
    fractals = mongo.db.fractals.find()
    return list(fractals)
