import logging
import os
import re
import shutil

import requests
from urllib.parse import unquote, urlparse

from unidecode import unidecode

from . import PresentationExportionUtils
from .LanguageHandler import LanguageHandler
from .Errors import InvalidPathError

MAIN_DIR = os.path.abspath(os.path.join(os.path.dirname(
    os.path.realpath(__file__)), '..'))

WORKING_DIR = os.path.join(MAIN_DIR, "working")

RESULTS_DIR = os.path.join(MAIN_DIR, "results")


def download_to_working(url: str) -> str:
    # checks if it already exists to return it.
    if os.path.exists(os.path.join(WORKING_DIR, url.split("\\")[-1])):
        return os.path.join(WORKING_DIR, url.split("\\")[-1])

    # Send a GET request
    try:
        response = requests.get(url, stream=True, verify=False)
    except Exception as e:
        raise ConnectionError("Check your Connection")

    logging.debug("request status code: %d" % response.status_code)

    # If the GET request is successful, the status code will be 200
    if response.status_code == 200:
        # Get the file name from the URL and decode it
        file_name = get_valid_name(url)

        # If the file is an HTML file
        is_text = False
        if 'text/html' in response.headers['content-type']:
            file_name = file_name + '.html' if '.html' not in file_name else file_name
            is_text = True
        # If the file is a PDF file
        elif 'application/pdf' in response.headers['content-type']:
            file_name = file_name + '.pdf' if '.pdf' not in file_name else file_name
        # If the file is an image file
        elif 'image/' in response.headers['content-type']:
            image_extension = response.headers['content-type'].split('/')[-1]
            file_name = file_name + '.' + image_extension \
                if '.' + image_extension not in file_name else file_name

        # Create a path for the new file
        file_path = os.path.join(WORKING_DIR, file_name)

        # Open the file in write mode
        if is_text:  # to handle encoding problems
            with open(file_path, 'w', encoding=response.encoding) as file:
                file.write(response.text)
        else:
            with open(file_path, 'wb') as file:
                shutil.copyfileobj(response.raw, file)

        return file_path
    else:
        logging.debug(f"Failed to retrieve the URL due to the status code: "
                      f"{response.status_code}")


def is_path_or_url(string) -> str:
    # Check if string is a local path
    if os.path.exists(string):
        return "Path"
    # Check if string is a URL
    elif urlparse(string).scheme in ["http", "https"]:
        return "URL"
    else:
        return "Unknown"


def copy_file_to_working(file_path) -> str:
    file_name = file_path.split(os.path.sep)[-1]

    # case: the file already exists in the working directory.
    if os.path.join(WORKING_DIR, file_name) == file_path:
        return file_path
    shutil.copy2(file_path, WORKING_DIR)
    return os.path.join(WORKING_DIR, file_name)


def get_file_name(working_path: str) -> str:
    return working_path.split(os.path.sep)[-1]


def get_valid_name(url):
    base_filename = url.rsplit("/", 1)[1]
    base_filename = unquote(base_filename)
    base_filename = unidecode(base_filename)
    import re

    filename = re.sub(r'[^\w\-_.]', '', base_filename)

    return filename


def uniquify(path):
    filename, extension = os.path.splitext(path)
    counter = 1

    while os.path.exists(path):
        path = filename + "_" + str(counter) + extension
        counter += 1

    return path


def divide_to_subarrays(str_list: list[str], sub_size: int) -> list[list[str]]:
    """
    divides an array to maximum number of sub-arrays with size at least
     equal to the given
    :param str_list: list of strings
    :param sub_size: the minimum size of a subarray
    :return: list of lists represents the divided sub-arrays
    """
    # Calculate the size of the first subarray
    first_sub_size = len(str_list) % sub_size
    if first_sub_size == 0:
        first_sub_size = sub_size

    # Create the first subarray
    subarrays = [str_list[:first_sub_size]]

    # Create the remaining subarrays
    for i in range(first_sub_size, len(str_list), sub_size):
        subarrays.append(str_list[i:i + sub_size])

    return subarrays


def split_text_to_sentences(text: str):
    """
    splits text on periods, also it differentiates between periods
     in decimal numbers and in shortcuts for names
    :param text: text to split
    :return: a list of sentences
    """
    split_res = re.split(r"(?<!\s\w\.\w)(?<!\s\w)\.(?!\d)\s+", text)
    res = []
    for snt in split_res:
        if len(snt) > 0:
            res.append(snt)
    return res


def divide_sentence(sentence: str, with_words):
    pattern = r",\s" + r"|,\s".join(with_words)
    return [sentence.strip() for sentence in re.split(pattern, sentence)]


def is_sentence_empty(sentence: str) -> bool:
    return sentence.strip(" \n\t\r") == ""


def clear_sentence(sentence: str) -> str:
    return sentence.strip(" \n\t\r")
