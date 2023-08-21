import validators
from flask import Blueprint, render_template, request, jsonify
from website import controller

view = Blueprint("view", __name__)

filesList = []


@view.route("/")
def home():
    return render_template("presentation_maker_webpage.html")


@view.route('/add-url', methods=["POST"])
def add_url():
    data = request.get_json()
    _url = data["url"]

    if _url == "":
        return jsonify({"success": False, "data_sent": data
                        , "message": "No URL given!"})

    if not validators.url(_url):
        return jsonify({"success": False, "data_sent": data
                        , "message": "URL is not valid, check your URL and try again."})

    filesList.append({"url": _url})

    return jsonify({"success": True, "filesList": filesList})


@view.route("/remove-url", methods=["POST"])
def remove_url():
    data = request.get_json()
    _url = data["url"]

    # removing the url.
    check = True
    ###

    if check:
        global filesList
        filesList = [file for file in filesList if file["url"] != _url]
        return jsonify({"success": True, "filesList": filesList})
    else:
        return jsonify({"success": False, "message": "Url Doesn't Exist"})


@view.route("/get-files", methods=["GET"])
def get_files():
    return jsonify(filesList)


@view.route("/remove-all-files", methods=["POST"])
def remove_all_files():
    global filesList
    filesList = []
    return jsonify({"success": True})


@view.route("/create-presentation", methods=["POST"])
def create_presentation():
    paths = [file["url"] for file in filesList]

    # call_controller
    output_file = controller.create_presentation(paths)

    # send the PowerPoint file to user

