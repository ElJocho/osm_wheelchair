import json
import requests
import numpy
from collections import defaultdict
from python.code.utils.definitions import logger

RESULT_PATH = "./data/result"

def get_ts(bpoly):

    request_url = f"https://api.ohsome.org/v1/elements/count/groupBy/tag?bpolys={bpoly}&filter=amenity%3D*%20and%20wheelchair%20in%20(yes%2Cno%2Climited)&format=json&groupByKey=wheelchair&time=2010-01-01%2F2021-01-01%2FP1Y"

    print("Downloading...")
    try:
        response = requests.post(request_url)
        response.raise_for_status()
        response_text = response.text
    except requests.exceptions.HTTPError as http_err:
        print(f'HTTP error: {http_err}')
    except Exception as err:
        print(f'Error occurred: {err}')

    response_json = json.loads(response.text)

    tags = []
    d = defaultdict(list)

    for i in response_json["groupByResult"]:
        tag = i["groupByObject"]
        tags.append(i["groupByObject"])

        for j in i["result"]:
            t = numpy.datetime64(j["timestamp"]).astype(float)*1000
            v = j["value"] 
            d[t].append(v)

    d = {"tagging":d}

    out_tags = json.dumps(tags)
    out_time_series = json.dumps(d) 

    with open(os.path.join(RESULT_PATH,"time_series.json") as ts_out:
        json.dumps(out_time_series)

    logger.info("dropped time series into results")