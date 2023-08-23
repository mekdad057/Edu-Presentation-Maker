import os

RESULTS_WEB_DIR = os.path.abspath(os.path.join(os.path.dirname(
    os.path.realpath(__file__)), 'static', 'results'))


def clear_results_folder():
    for file_object in os.listdir(RESULTS_WEB_DIR):
        file_object_path = os.path.join(RESULTS_WEB_DIR, file_object)
        if os.path.isfile(file_object_path) or os.path.islink(file_object_path):
            os.unlink(file_object_path)
