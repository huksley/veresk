"""Web app entrypoint"""

import connexion
from flask import redirect, render_template
from plot import bp as plot_bp

app = connexion.FlaskApp(__name__)
app.add_api("api.yaml")
app.app.register_blueprint(plot_bp)


@app.route("/")
def root():
    return redirect("/index.html", 302)


@app.route("/index.html")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(port=8080)
