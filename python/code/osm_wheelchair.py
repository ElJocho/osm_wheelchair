"""
download+parse ohsome data
args: bounding-geojson path | scoring csv path
output: geojson with added tags wheelchair score (from scoring matrix),
wheelchair tags (# of tags from csv),
json obj with relationship of features with/without relevant tags

TODO: adjust path to project
"""

import sys
import csv
import json
from geojson import FeatureCollection
import geojson
import requests
from pathlib import Path
import os
from python.code.utils.ohsome import query
from python.code.utils.definitions import logger
from os import walk
from python.code.utils.utils import to_json

# define some basic variables
INPUT_PATH = "./data/input"
RESULT_PATH = "./data/result"
GEOJSON_PATH = "./data/geojson"
AREA_OF_INTEREST_PATH = "./data/areas_of_interest"
csv_path = os.path.join(INPUT_PATH, "tabelle_2.csv")
geojson_path = os.path.join(INPUT_PATH, "area_of_interest.geojson")

names = ["roads_geoms", "pois_geoms", "aois_geoms"]

# define ohsome query endpoints

roads = {
    "description": "roads",
    "endpoint": "elements/geometry",
    "filter": """
        geometry:line 
        and highway=*
    """
}

pois = {
    "description": "Points of Interest for daily life or tourism",
    "endpoint": "elements/geometry",
    "filter": """
      geometry:point and (
          highway=bus_stop or railway=station or
          shop=* or tourism in (hotel, attraction) or
          amenity in (fuel, pharmacy, hospital, school, college, university,
          police, fire_station, restaurant, townhall)
      )
    """
}

aois = {
    "description": "Areas of Interest for daily life or tourism",
    "endpoint": "elements/geometry",
    "filter": """
      geometry:polygon and (
          highway=bus_stop or railway=station or
          shop=* or tourism in (hotel, attraction) or
          amenity in (fuel, pharmacy, hospital, school, college, university,
          police, fire_station, restaurant, townhall)
      )
    """
}


def read_csv(csv_path):
    scores = []
    with open(csv_path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        for key, value, score in csv_reader:
            scores.append([key, value, float(score)])

    return scores


def load_ohsome_layers(geojson_path, csv_path, geojson_outpath):
    with open(geojson_path, encoding="utf8") as infile:
        analysis_area = geojson.load(infile)
        analysis_area = geojson.dumps(analysis_area)

    roads_geoms = query(request=roads, bpolys=analysis_area, properties="tags")
    pois_geoms = query(request=pois, bpolys=analysis_area, properties="tags")
    aois_geoms = query(request=aois, bpolys=analysis_area, properties="tags")

    dimensions = [roads_geoms, pois_geoms, aois_geoms]
    for x in range(0, len(names)):
        with open(os.path.join(geojson_outpath, names[x] + ".geojson"), "w") as outpath:
            geojson.dump(dimensions[x], outpath)
    logger.info("dropped ohsome result into geojson folder.")
    return dimensions


def score_layer(dimensions=None, geojson_outpath=None, result_outpath=None):

    #  load from file if we do not download and pass them
    if dimensions is None:
        dimensions = []
        for name in names:
            file_path = os.path.join(geojson_outpath, name + ".geojson")
            with open(file_path, "r") as infile:
                dimensions.append(geojson.load(infile))

    scores = read_csv(csv_path)
    wh_yes = 0
    wh_limited = 0
    wh_no = 0
    untagged = 0

    polys = []
    points = []
    lines = []
    for x in range(0, len(dimensions)):
        for feature in dimensions[x]["features"]:
            props = feature["properties"]
            feature_score = []
            tot_score = None

            for key, val in props.items():

                for score_k, score_v, score in scores:

                    if (str(key) == "wheelchair" and str(val) == "no"):
                        wh_no += 1
                    if (str(key) == "wheelchair" and str(val) == "limited"):
                        wh_limited += 1
                    if (str(key) == "wheelchair" and str(val) == "yes"):
                        wh_yes += 1
                        feature_score = [1]
                        break
                    elif score_k == key and score_v == val:
                        feature_score.append(score)

            if len(feature_score) > 0:
                if -1 in feature_score:
                    tot_score = -1
                tot_score = sum(feature_score) / len(feature_score)
            else:
                tot_score = -2
                untagged += 1

            props["wheelchair_tags"] = len(feature_score)
            props["wheelchair_score"] = tot_score
            feature["properties"] = props

        with open(os.path.join(result_outpath, names[x] + ".geojson"), "w") as outpath:
            geojson.dump(dimensions[x], outpath)
    """
    tagging_rel = {
        'tagging_relationship': {'yes': wh_yes, 'limited': wh_limited, 'no': wh_no,
                                 'untagged': untagged}}

    with open(f"{out_basepath}/{out_basename}_tags.json", "w") as outtags:
        json.dump(tagging_rel, outtags)
    """




def execute_workflow(download: bool = False):
    _, _, filenames = next(walk(AREA_OF_INTEREST_PATH))
    f = []
    for file in filenames:
        f.append(file[:-8])
        result_outpath = os.path.join(RESULT_PATH,file[:-8])
        geojson_outpath = os.path.join(GEOJSON_PATH,file[:-8])

        if not os.path.exists(geojson_outpath):
            os.mkdir(geojson_outpath)
            os.mkdir(result_outpath)

        geojson_inpath = os.path.join(AREA_OF_INTEREST_PATH, file)
        dimensions = None
        if download:
            dimensions = load_ohsome_layers(geojson_inpath, csv_path, geojson_outpath)
        score_layer(dimensions, geojson_outpath, result_outpath)
    to_json(os.path.join(RESULT_PATH, "valid_dirs.json"), "dirs", f)
execute_workflow(download=True)