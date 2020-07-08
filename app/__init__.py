from pymongo import ASCENDING
from flask import redirect, render_template
from connexion import FlaskApp
import os
from flask_pymongo import PyMongo
from app.plot import bp as plot_bp
from flask import current_app

import app.classes.MongoJSONEncoder as MongoJSONEncoder
import app.classes.ObjectIdConverter as ObjectIdConverter


app = FlaskApp(__name__)
app.add_api("api.yaml")
app.app.register_blueprint(plot_bp)
app.app.json_encoder = MongoJSONEncoder
app.app.url_map.converters['objectid'] = ObjectIdConverter
app.app.config['TEMPLATES_AUTO_RELOAD'] = True
app.app.config["MONGO_URI"] = os.environ['MONGO_URI']
mongo = PyMongo(app.app)

try:
    mongo.db.users.create_index([('userName', ASCENDING)], unique=True)
except Exception as e:
    print("Failed to create indexes: ", e)


@app.route("/")
def root():
    return redirect("/index.html", 302)


@app.route("/index.html")
def index():
    all_users = list(mongo.db.users.find())
    return render_template("index.html", users=all_users)


def get_mongo():
    return mongo


def get_app():
    return app
