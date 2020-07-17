"""Classes to assist in conversion between MongoDB specific datatypes and JSON compatible ones"""

from datetime import datetime, date
import isodate as iso
from bson import ObjectId
from flask.json import JSONEncoder
from werkzeug.routing import BaseConverter


class MongoJSONEncoder(JSONEncoder):
    """Convert MongoDB dates and objectId to string value and back"""

    def default(self, o):
        if isinstance(o, (datetime, date)):
            return iso.datetime_isoformat(o)
        if isinstance(o, ObjectId):
            return str(o)
        return super().default(o)


class ObjectIdConverter(BaseConverter):
    """Convert MongoDB ObjectID to string value and back"""

    def to_python(self, value):
        return ObjectId(value)

    def to_url(self, value):
        return str(value)
