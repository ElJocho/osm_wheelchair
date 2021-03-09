import datetime
from typing import Dict

import requests

from python.code.utils.definitions import OHSOME_API, logger


def query(request: Dict, bpolys: str, properties: str = None, time_range=None) -> Dict:
    """Query ohsome API endpoint with filter."""
    url = OHSOME_API + request["endpoint"]
    if properties is not None:
        data = {"bpolys": bpolys, "filter": request["filter"], "properties": properties}
    elif time_range is not None:
        data = {"bpolys": bpolys, "filter": request["filter"], "time": time_range}
    else:
        data = {"bpolys": bpolys, "filter": request["filter"]}


    logger.info("Query to the ohsome API.")
    logger.info("URL: " + url)
    logger.info("Filter: " + request["filter"])

    response = requests.post(url, data=data)

    if response.status_code == 200:
        logger.info("Query successful!")
    elif response.status_code == 404:
        logger.info("Query failed!")
    else:
        logger.info(response)

    return response.json()

