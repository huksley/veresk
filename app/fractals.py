"""Fractal CRUD management"""

from pymongo.errors import DuplicateKeyError
from bson import ObjectId


def fractals_add(**request):
    """Add new fractal"""
    body = request["body"]
    print("Adding fractal", body)
    try:
        from app import get_mongo #pylint: disable=import-outside-toplevel
        mongo = get_mongo()
        saved = mongo.db.fractals.insert_one({
            "complex_real": body["complex_real"],
            "complex_imaginary": body["complex_imaginary"]
        })
        print("Added fractal", saved.inserted_id)
        return None
    except DuplicateKeyError as err:
        print("Failed to add new fractal:", err)
        return (None, 409)


def fractals_update(fractal_id, **request):
    """Update existing fractal"""
    body = request["body"]
    print("Updating fractal", body, "id", fractal_id)
    try:
        from app import get_mongo #pylint: disable=import-outside-toplevel
        mongo = get_mongo()
        saved = mongo.db.fractals.update_one({"_id": ObjectId(fractal_id)}, {"$set": {
            "complex_real": body["complex_real"],
            "complex_imaginary": body["complex_imaginary"]
        }})
        print("Updated fractal", fractal_id, "matches", saved.matched_count)
        return None
    except DuplicateKeyError as err:
        print("Failed to update fractal:", err)
        return (None, 409)


def fractals_delete(fractal_id):
    """Delete existing fractal"""
    print("Deleting fractal", fractal_id)
    from app import get_mongo #pylint: disable=import-outside-toplevel
    mongo = get_mongo()
    saved = mongo.db.fractals.delete_one({"_id": ObjectId(fractal_id)})
    print("Delete fractal", fractal_id, "matches", saved.deleted_count)

def fractals_list():
    """List all fractals"""
    from app import get_mongo #pylint: disable=import-outside-toplevel
    mongo = get_mongo()
    fractals = mongo.db.fractals.find()
    return list(fractals)
