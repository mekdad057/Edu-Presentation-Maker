import os

import validators
from flask import Blueprint, render_template, request, jsonify, send_file
from website import controller, WEBSITE_DIR

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

    if _url in filesList:
        return jsonify({"success": False, "data_sent": data
                        , "message": "URL already exists, try again with another URL"})

    filesList.append(_url)

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
        filesList = [url for url in filesList if url != _url]
        return jsonify({"success": True, "filesList": filesList})
    else:
        return jsonify({"success": False, "message": "Url Doesn't Exist"})


@view.route("/get-files", methods=["GET"])
def get_files():
    return jsonify({"filesList": filesList})


@view.route("/remove-all-files", methods=["POST"])
def remove_all_files():
    global filesList
    filesList = []
    return jsonify({"success": True})


@view.route("/create-presentation", methods=["POST"])
def create_presentation():
    data = request.get_json()
    title = data["title"]
    paths = filesList

    if title and paths:
        controller.create_presentation(title, paths, WEBSITE_DIR)
        return jsonify({"success": True, "message": "Presentation created successfully"})
    else:
        return jsonify({"success": False, "message": "you have to enter a title and some urls!"})


@view.route("/download-presentation", methods=["GET"])
def download_presentation():
    # returning the first file in the Website directory that has pptx
    # extension which the required file
    files = [each for each in os.listdir(WEBSITE_DIR) if each.endswith('.pptx')]
    if not files:
        return jsonify({"success": True, "message": "the file is not ready"})
    output_file_path = files[0]
    return send_file(output_file_path)
