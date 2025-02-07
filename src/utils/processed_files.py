import os

from definitions import PROCESSED_DIR


def save_to_processed(filename, header, lines):
    """
    Saves the fetched data to a file in the processed directory.
    :param header: Header line.
    :param lines: Data to be saved.
    :param filename: Name of the file.
    """
    filepath = os.path.join(PROCESSED_DIR, filename)
    f = open(filepath, "w")
    f.write(f"{header}\n")
    for line in lines:
        f.write(f"{line}\n")
    f.close()
