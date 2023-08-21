from flask import Flask

from website.Controller import Controller

controller = Controller()


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "6548484531"

    from .view import view

    app.register_blueprint(view)

    return app
