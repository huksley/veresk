"""Web app entrypoint"""

from plot import bp as plot_bp
from flask_pymongo import PyMongo
from flask import redirect, render_template
import connexion
import os

app = connexion.FlaskApp(__name__)
app.add_api("api.yaml")
app.app.register_blueprint(plot_bp)
app.app.config['TEMPLATES_AUTO_RELOAD'] = True
app.app.config["MONGO_URI"] = os.environ['MONGO_URI'] or "mongodb://localhost:27017/myDatabase"
mongo = PyMongo(app.app)


@app.route("/")
def root():
    return redirect("/index.html", 302)


@app.route("/index.html")
def index():
    all_users = mongo.db.users.find()
    return render_template("index.html", context={
        "users": all_users
    })


if __name__ == "__main__":
    app.run(port=8080)
