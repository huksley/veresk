"""Veresk web application"""

import os
from hashlib import sha256
from flask import redirect, render_template, send_from_directory, request, url_for, session, Response
from connexion import FlaskApp
from flask_pymongo import PyMongo
from flask_dance.contrib.github import make_github_blueprint, github

from pymongo import ASCENDING
from pymongo.errors import PyMongoError
from bson import ObjectId

from .plot import bp as plot_bp
from .helpers import MongoJSONEncoder, ObjectIdConverter


app = FlaskApp(__name__)
app.add_api("api.yaml")
app.app.secret_key = os.environ['FLASK_SECRET_KEY']
app.app.register_blueprint(plot_bp)
app.app.json_encoder = MongoJSONEncoder
app.app.url_map.converters['objectid'] = ObjectIdConverter


def dev():
    """Detect dev environment"""
    return os.environ.get("AWS_EXECUTION_ENV") is None


app.app.config['TEMPLATES_AUTO_RELOAD'] = 1 if dev() else 0

if dev():
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

if os.environ["GITHUB_OAUTH_CLIENT_ID"] is not "":
    oauth_blueprint = make_github_blueprint(
        client_id=os.environ[("" if dev() else "PROD_") +
                            "GITHUB_OAUTH_CLIENT_ID"],
        client_secret=os.environ[("" if dev() else "PROD_") +
                                "GITHUB_OAUTH_CLIENT_SECRET"],
    )
    app.app.register_blueprint(oauth_blueprint, url_prefix="/login")

app.app.config["MONGO_URI"] = os.environ['MONGO_URI']
mongo = PyMongo(app.app)


@app.app.after_request
def remove_if_invalid(response):
    """Invalidate Flask session, if specified so at the end of the request"""
    if "__invalidate__" in session:
        response.delete_cookie(app.app.session_cookie_name)
    return response


def get_user_hash():
    """
    Return hashed ID of user.
    Locally we use 0 to indicate root, remotely we indicate None for anonymous.
    """
    if os.environ["GITHUB_OAUTH_CLIENT_ID"] is "":
        return None
    if not github.authorized:
        return None
    user_hash = sha256()
    user_hash.update(app.app.secret_key.encode('utf-8'))
    resp = github.get("/user")
    user_hash.update(str(resp.json()["id"]).encode('utf-8'))
    return user_hash.hexdigest()


@app.route("/")
def root():
    """Root page"""
    fractals = list(mongo.db.fractals.find())
    content = render_template("index.html", fractals=fractals, github=github, dev=dev(), user_hash=get_user_hash())
    resp = Response(content)
    resp.headers['Strict-Transport-Security'] = 'max-age=63072000' # 2 years
    return resp


@app.route("/user")
def user():
    """Root page"""
    if os.environ["GITHUB_OAUTH_CLIENT_ID"] is "":
        return ("No login support", 200)
    if not github.authorized:
        return redirect(url_for("github.login"))
    resp = github.get("/user")
    print("User", resp.json())
    assert resp.ok
    return "You are @{login} on GitHub".format(login=resp.json()["login"])


@app.route("/logout")
def logout():
    """Logout from app. Does not removes OAuth enrollement."""
    session["__invalidate__"] = True
    return redirect(url_for("index"))


@app.route("/favicon.ico")
def favicon():
    """Redirect to proper favicon"""
    return redirect("static/icon.svg", code=302)


@app.route('/robots.txt')
@app.route('/site.webmanifest')
def static_from_root():
    """Mapping for static files"""
    return send_from_directory(app.app.static_folder, request.path[1:])


@app.route('/share/<string:fractal_id>')
def share(fractal_id):
    """Share fractal page"""
    fractal = mongo.db.fractals.find_one({
        "_id": ObjectId(fractal_id)
    })
    if fractal is None:
        print("Cant find fractal", fractal_id)
        return ("Not found", 404)
    return render_template("share.html", fractal=fractal, github=github, dev=dev(), user_hash=get_user_hash())

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
