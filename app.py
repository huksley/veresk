"""Web app entrypoint"""

from flask import redirect, render_template
from config import get_app, get_mongo
from pymongo import ASCENDING

app = get_app()
mongo = get_mongo()

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


if __name__ == "__main__":
    app.run(port=8080)
