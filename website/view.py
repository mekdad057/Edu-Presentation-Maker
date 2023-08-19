import validators
from flask import Blueprint, render_template, request, jsonify

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
    # processing the request
    check, name, size_in_mb = True, "Document Name", 5.2
    ###

    filesList.append({"fileName": name, "fileSize": size_in_mb})
    if check:
        return jsonify({"success": True, "filesList": filesList})
    else:
        return jsonify({"success": False, "data_sent": data
                        , "message": "adding URL failed, please try again."})


@view.route("/remove-url", methods=["POST"])
def remove_url():
    data = request.get_json()
    name = data["name"]

    # removing the url.
    check = True
    ###

    if check:
        global filesList
        filesList = [file for file in filesList if file["fileName"] != name]
        return jsonify({"success": True, "filesList": filesList})
    else:
        return jsonify({"success": False, "message": "Url Doesn't Exist"})


@view.route("/get-files", methods=["GET"])
def get_files():
    return jsonify(filesList)
