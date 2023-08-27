import os.path

import validators
from flask import Blueprint, render_template, request, jsonify, \
    send_from_directory
from website import controller
from website.config import RESULTS_WEB_DIR

view = Blueprint("view", __name__)

files_list = []
result_path = ""


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

    if _url in files_list:
        return jsonify({"success": False, "data_sent": data
                           ,"message": "URL Already Exists!"})

    files_list.append(_url)

    return jsonify({"success": True, "filesList": files_list})


@view.route("/remove-url", methods=["POST"])
def remove_url():
    data = request.get_json()
    _url = data["url"]

    # removing the url.
    check = True
    ###

    if check:
        global files_list
        files_list = [url for url in files_list if url != _url]
        return jsonify({"success": True, "filesList": files_list})
    else:
        return jsonify({"success": False, "message": "Url Doesn't Exist"})


@view.route("/get-files", methods=["GET"])
def get_files():
    return jsonify(files_list)


@view.route("/remove-all-files", methods=["POST"])
def remove_all_files():
    global files_list
    global result_path
    files_list = []
    result_path = ""
    return jsonify({"success": True})


@view.route("/create-presentation", methods=["POST"])
def create_presentation():
    global result_path
    data = request.get_json()
    title = data.get("title", None)
    presentation_type = data.get("presentationType", None)

    if not title or not presentation_type or len(files_list) == 0:
        return jsonify({"success": False, "message": "Enter all required data."})

    if result_path != "":
        return jsonify({"success": False, "message": "press Clear first."})

    result_path = controller.create_presentation(title, files_list, presentation_type)

    return jsonify({"success": True
                    , "message": "Presentation is ready to be downloaded"
                    })


@view.route("/download", methods=["GET"])
def download():
    if result_path == "":
        return jsonify({"success": False
                            , "message": "Create a Presentation First"
                        })
    if not os.path.exists(result_path):
        return jsonify({"success": False
                           , "message": f"File Does Not Exist"
                        })
    return send_from_directory(RESULTS_WEB_DIR
                               , os.path.basename(result_path)
                               , as_attachment=True)


@view.route("/get-file-name")
def get_file_name():
    global result_path
    return jsonify({"fileName": result_path})
