import os
import json
from python.code.utils.definitions import DATA_PATH, logger


def to_json(filename, key, value):
    """Drop results."""

    try:
        with open(filename) as file:
            data = json.load(file)
    except FileNotFoundError:
        logger.info(
            "File {} not existing. Creating a new one.".format(
                filename
            )
        )
        data = {}

    data[key] = value

    with open(filename, "w") as f:
        json.dump(data, f)
