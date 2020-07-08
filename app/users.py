"""User management"""

from pymongo.errors import DuplicateKeyError
from bson import ObjectId


def users_add(**request):
    """Add new user"""
    user = request["body"]
    print("Adding user", user)
    try:
        from app import get_mongo #pylint: disable=import-outside-toplevel
        mongo = get_mongo()
        saved = mongo.db.users.insert_one({
            "userName": user["userName"]
        })
        print("Added user", saved.inserted_id)
        return None
    except DuplicateKeyError as err:
        print("Failed to add new user:", err)
        return (None, 409)


def users_update(user_id, **request):
    """Update existing user"""
    user = request["body"]
    print("Updating user", user, "id", user_id)
    try:
        from app import get_mongo #pylint: disable=import-outside-toplevel
        mongo = get_mongo()
        saved = mongo.db.users.update_one({"_id": ObjectId(user_id)}, {"$set": {
            "userName": user["userName"]
        }})
        print("Updated user", user_id, "matches", saved.matched_count)
        return None
    except DuplicateKeyError as err:
        print("Failed to add new user:", err)
        return (None, 409)


def users_delete(user_id):
    """Delete existing user"""
    print("Deleting user", user_id)
    from app import get_mongo #pylint: disable=import-outside-toplevel
    mongo = get_mongo()
    saved = mongo.db.users.delete_one({"_id": ObjectId(user_id)})
    print("Delete user", user_id, "matches", saved.deleted_count)

def users_list():
    """List all users"""
    from app import get_mongo #pylint: disable=import-outside-toplevel
    mongo = get_mongo()
    all_users = mongo.db.users.find()
    return list(all_users)
