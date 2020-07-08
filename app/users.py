from pymongo.errors import DuplicateKeyError
from bson import ObjectId


def users_add(**request):
    """Add new user"""
    user = request["body"]
    print("Adding user", user)
    try:
        from app import get_mongo
        mongo = get_mongo()
        saved = mongo.db.users.insert_one({
            "userName": user["userName"]
        })
        print("Added user", saved.inserted_id)
        return None
    except DuplicateKeyError as err:
        print("Failed to add new user:", err)
        return (None, 409)


def users_update(id, **request):
    """Update existing user"""
    user = request["body"]
    print("Updating user", user, "id", id)
    try:
        from app import get_mongo
        mongo = get_mongo()
        saved = mongo.db.users.update_one({"_id": ObjectId(id)}, {"$set": {
            "userName": user["userName"]
        }})
        print("Updated user", id, "matches", saved.matched_count)
        return None
    except DuplicateKeyError as err:
        print("Failed to add new user:", err)
        return (None, 409)


def users_delete(id):
    """Delete existing user"""
    print("Deleting user", id)
    from app import get_mongo
    mongo = get_mongo()
    saved = mongo.db.users.delete_one({"_id": ObjectId(id)})
    print("Delete user", id, "matches", saved.deleted_count)
    return None


def users_list(**request):
    """List all users"""
    from app import get_mongo
    mongo = get_mongo()
    all_users = mongo.db.users.find()
    return list(all_users)
