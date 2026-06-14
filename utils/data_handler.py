import json
import os

DATA_DIR = "data"


def get_file_path(filename):
    return os.path.join(DATA_DIR, filename)


def read_json(filename, default):
    path = get_file_path(filename)

    if not os.path.exists(path):
        write_json(filename, default)
        return default

    try:
        with open(path, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return default


def write_json(filename, data):
    path = get_file_path(filename)

    with open(path, "w") as f:
        json.dump(data, f, indent=4)