from flask import Flask

from website.Controller import Controller
from website.Model import Model


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "6548484531"

    from .view import view
    app.register_blueprint(view)

    return app


# single objects
model = Model()
controller = Controller(model)
