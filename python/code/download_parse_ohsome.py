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
import requests
from pathlib import Path
import os

def read_csv(csv_path):

    with open(csv_path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        for key,value,score in csv_reader:
            print("scoring:", key,value,score)

    return  key,value,float(score)


def downloadData(bpoly_path):

    with open(bpoly_path) as bpoly_file:
        bpoly = bpoly_file.read()

    request_url = f"https://api.ohsome.org/v1/elements/geometry?bpolys={bpoly}&clipGeometry=true&filter=type%3Away%20and%20highway%3D*&properties=tags&time=2021-01-01&timeout=60"

    print("Downloading...")
    try:
        response = requests.post(request_url)
        response.raise_for_status()
        response_text = response.text
    except requests.exceptions.HTTPError as http_err:
        print(f'HTTP error: {http_err}')
    except Exception as err:
        print(f'Error occurred: {err}')

    data = json.loads(response_text)

    return data


def parseJson(bpoly_path,csv_path):

    data = downloadData(bpoly_path)
    score_k,score_v,score = read_csv(csv_path)

    tagged = 0
    untagged = 0

    for i in data["features"]:
        geom = i["geometry"]["coordinates"] 
        props = i["properties"] 
        feature_score = []

        for key,val in props.items():

            if score_k == key and score_v == val:
                feature_score.append(score)
            else: 
                continue

        if -1 not in feature_score:
            tot_score = sum(feature_score)
        else: 
            tot_score = -1

        props["wheelchair_score"] = tot_score

        if len(feature_score) == 0:
            tot_score = -2
            untagged += 1
        else:
            props["wheelchair_tags"] = len(feature_score)
            tagged += 1

    tagging_rel = {'tagging_relationship':{'tagged_cnt':tagged, 'untagged_cnt':untagged}}

    outfile = Path(bpoly_path).stem
    outpath = os.path.join(os.path.dirname(__file__), "output")

    with open(f"{outpath}/{outfile}_data.geojson", "w") as outfile:
        json.dump(data, outfile)

    with open(f"{outpath}/{outfile}_tags.geojson", "w") as outfile:
        json.dump(tagging_rel, outfile)

if __name__ == "__main__":
    bpoly_path = sys.argv[0]
    csv_path = sys.argv[1]
    parseJson(bpoly_path,csv_path)
