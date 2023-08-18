from flask import Blueprint, render_template,stream_template_string

view = Blueprint("view", __name__)


@view.route("/")
def home():
    return render_template("presentation_maker_webpage.html")
