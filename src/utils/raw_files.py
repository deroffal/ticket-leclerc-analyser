import json
import os

from definitions import RAW_DIR


def raw_file_exists(filename) -> bool:
    """:returns true if a file named as specified exists in raw directory"""
    return os.path.isfile(f"{RAW_DIR}/{filename}")


def save_to_raw(filename, data):
    """
    Saves the fetched data to a file in the raw directory.
    :param data: Data to be saved.
    :param filename: Name of the file.
    """
    filepath = os.path.join(RAW_DIR, filename)
    with open(filepath, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)


def list_raw_files():
    """
    List directory's files name
    :return: Returns all files name in the directory
    """
    return [f for f in next(os.walk(RAW_DIR), (None, None, []))[2] if f.endswith(".html")]


def open_raw_file(_filename):
    return open(f"{RAW_DIR}/{_filename}", "r")

