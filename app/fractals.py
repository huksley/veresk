"""Fractal CRUD management"""

from pymongo.errors import DuplicateKeyError
from bson import ObjectId


def fractals_add(**request):
    """Add new fractal"""
    from . import get_mongo, dev, get_user_hash  # pylint: disable=import-outside-toplevel

    if dev() is None and get_user_hash() is None:
        print("Forbidden to create in the cloud for user:", get_user_hash())
        return (None, 403)

    body = request["body"]
    print("Adding fractal", body)
    mongo = get_mongo()
    try:
        saved = mongo.db.fractals.insert_one({
            "complex_real": body["complex_real"],
            "complex_imaginary": body["complex_imaginary"],
            "user": get_user_hash()
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
    from . import get_mongo, get_user_hash, dev  # pylint: disable=import-outside-toplevel
    mongo = get_mongo()
    try:
        existing = mongo.db.fractals.find_one({
            "_id": ObjectId(fractal_id)
        })
        if dev() or existing["user"] != get_user_hash():
            print("Update: Not found or no access: ",
                  fractal_id, "user", get_user_hash())
            return (None, 403)
        saved = mongo.db.fractals.update_one({"_id": ObjectId(fractal_id)}, {"$set": {
            "complex_real": body["complex_real"],
            "complex_imaginary": body["complex_imaginary"]
        }})
        print("Updated fractal", fractal_id, "matches", saved.matched_count, "user", get_user_hash())
    except DuplicateKeyError as err:
        print("Failed to update fractal:", err)
        return (None, 409)
    return None


def fractals_delete(fractal_id):
    """Delete existing fractal"""
    print("Deleting fractal", fractal_id)
    from . import get_mongo, get_user_hash, dev  # pylint: disable=import-outside-toplevel
    mongo = get_mongo()
    existing = mongo.db.fractals.find_one({
        "_id": ObjectId(fractal_id)
    })
    if dev() or existing["user"] != get_user_hash():
        print("Delete: Not found or no access: ",
              fractal_id, "user", get_user_hash())
        return (None, 403)
    saved = mongo.db.fractals.delete_one({"_id": ObjectId(fractal_id)})
    print("Delete fractal", fractal_id, "matches", saved.deleted_count)
    return (None, 204)


def fractals_list():
    """List all fractals"""
    from . import get_mongo  # pylint: disable=import-outside-toplevel
    mongo = get_mongo()
    fractals = mongo.db.fractals.find()
    return list(fractals)
