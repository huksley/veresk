"""Veresk web application"""

import os

from flask import redirect, render_template, send_from_directory, request
from connexion import FlaskApp
from flask_pymongo import PyMongo

from pymongo import ASCENDING
from pymongo.errors import PyMongoError

from .plot import bp as plot_bp
from .helpers import MongoJSONEncoder, ObjectIdConverter


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


@app.route("/favicon.ico")
def favicon():
    """Redirect to proper favicon"""
    return redirect("static/icon.svg", code=302)


@app.route('/robots.txt')
@app.route('/site.webmanifest')
def static_from_root():
    return send_from_directory(app.app.static_folder, request.path[1:])


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
