"""Veresk web application"""

import os

from flask import redirect, render_template
from connexion import FlaskApp
from flask_pymongo import PyMongo

from pymongo import ASCENDING
from pymongo.errors import PyMongoError

from app.plot import bp as plot_bp

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

@app.route("/")
def root():
    """Root page"""
    fractals = list(mongo.db.fractals.find())
    return render_template("index.html", fractals=fractals)


@app.route("/index.html")
def index():
    """Old root page"""
    return redirect(".", 302)


def get_mongo():
    """Get PyMongo instance"""
    return mongo


def get_app():
    """Get Connexion app instance"""
    return app

