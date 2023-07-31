import logging
import os
import shutil

import requests
from urllib.parse import unquote, urlparse

from unidecode import unidecode

from .LanguageHandler import LanguageHandler
from .Errors import InvalidPathError

MAIN_DIR = os.path.abspath(os.path.join(os.path.dirname(
    os.path.realpath(__file__)), '..'))

WORKING_DIR = os.path.join(MAIN_DIR, "working")

RESULTS_DIR = os.path.join(MAIN_DIR, "results")


def download_to_working(url: str) -> str:
    # Send a GET request
    try:
        response = requests.get(url, stream=True, verify=False)
    except Exception as e:
        raise ConnectionError("Check your Connection")

    # If the GET request is successful, the status code will be 200
    if response.status_code == 200:
        # Get the file name from the URL and decode it
        file_name = url.split("/")[-1]
        file_name = unquote(file_name)
        file_name = unidecode(file_name)

        # If the file is an HTML file
        if 'text/html' in response.headers['content-type']:
            file_name = file_name + '.html' if '.html' not in file_name else file_name
        # If the file is a PDF file
        elif 'application/pdf' in response.headers['content-type']:
            file_name = file_name + '.pdf' if '.pdf' not in file_name else file_name

        # Create a path for the new file
        file_path = os.path.join(WORKING_DIR, file_name)

        # Open the file in write mode
        with open(file_path, 'wb') as file:
            # Write the content to the file
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    file.write(chunk)
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
