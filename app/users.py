from . import mongo


def add(**user):
    """Add new user"""
    print("Adding user", user["body"])
    return None
