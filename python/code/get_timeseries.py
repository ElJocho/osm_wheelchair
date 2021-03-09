import json
import requests
import numpy
from collections import defaultdict
from python.code.utils.definitions import logger
import geojson
import os
from python.code.utils.ohsome import query


def get_timeseries(bpoly, result_out_path):
    with open(bpoly, encoding="utf8") as infile:
        analysis_area = geojson.load(infile)
        analysis_area = geojson.dumps(analysis_area)
    request_url = f"https://api.ohsome.org/v1/elements/count/groupBy/tag?bpolys={analysis_area}&filter=amenity%3D*%20and%20wheelchair%20in%20(yes%2Cno%2Climited)&format=json&groupByKey=wheelchair&time=2010-01-01%2F2021-01-01%2FP1Y"

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

    with open(os.path.join(result_out_path,"time_series.json"), "w") as ts_out:
        json.dump(d, ts_out)

    logger.info("dropped time series into results")


tagged_highways_count = {
    "description": "all highways with relevant tags",
    "endpoint":"elements/count",
    "filter":"geometry:line and highway=* and (surface=* or smoothness=* or footwalk = *)"
}

all_highways = {
    "description": "highways",
    "endpoint": "elements/count",
    "filter": """
        geometry:line 
        and highway=*
    """
}

def get_num_relevant_tags(aoi, result_out_path):
    with open(aoi, encoding="utf8") as infile:
        analysis_area = geojson.load(infile)
        analysis_area = geojson.dumps(analysis_area)

    time_range = "2014-01-01/2021-01-01/P1Y"
    all_roads_count = query(all_highways, bpolys=analysis_area, time_range=time_range)
    tagged_highways = query(tagged_highways_count, bpolys=analysis_area, time_range=time_range)

    result = {}
    for element in range(0, len(all_roads_count["result"])):
        timestamp = all_roads_count["result"][element]["timestamp"]
        timestamp = numpy.datetime64(timestamp).astype(float) * 1000
        all_roads =  all_roads_count["result"][element]["value"]
        all_tagged  = tagged_highways["result"][element]["value"]
        result_value = all_tagged/all_roads * 100
        result[timestamp] = result_value

    out_data = {"share_tagged": result}
    with open(os.path.join(result_out_path,"share_tags.json"), "w") as ts_out:
        json.dump(out_data, ts_out)