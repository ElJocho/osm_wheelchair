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
import requests
from pathlib import Path
import os

def read_csv(csv_path):

    scores = []
    with open(csv_path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        for key,value,score in csv_reader:
            scores.append([key,value,float(score)])

    return scores

def parseJson(geojson_path,csv_path):

    with open(geojson_path, encoding="utf8") as g:
        gs_string = g.read()

    data = json.loads(gs_string)

    scores = read_csv(csv_path)
    
    wh_yes = 0
    wh_limited=  0
    wh_no = 0
    untagged = 0

    polys = []
    points = []
    lines = []


    for i in data["features"]:
        geomtype = i["geometry"]["type"] 
        props = i["properties"] 
        feature_score = []
        tot_score = None 
        
        for key,val in props.items():
            
            for score_k,score_v,score in scores:

                if(str(key) == "wheelchair" and str(val) == "no"):
                    wh_no += 1
                if(str(key) == "wheelchair" and str(val) == "limited"):
                    wh_limited += 1
                if(str(key) == "wheelchair" and str(val) == "yes"):
                    wh_yes += 1
                    feature_score = [1]
                    break
                elif score_k == key and score_v == val:
                    feature_score.append(score)

        if len(feature_score) > 0:
            if -1 in feature_score:
                tot_score = -1
            tot_score = sum(feature_score)/len(feature_score)
        else:
            tot_score = -2
            untagged += 1

        props["wheelchair_tags"] = len(feature_score)
        props["wheelchair_score"] = tot_score

        if(geomtype == "Point"):
            points.append(i)
        elif(geomtype == "Polygon"):
            polys.append(i)
        elif(geomtype == "LineString"):
            lines.append(i)

    points = FeatureCollection(points)
    polys = FeatureCollection(polys)
    lines = FeatureCollection(lines)

    tagging_rel = {'tagging_relationship':{'yes':wh_yes, 'limited':wh_limited, 'no':wh_no, 'untagged':untagged}}

    out_basename = Path(geojson_path).stem
    out_basepath = os.path.join(os.path.dirname(__file__), "../../data/result")

    with open(f"{out_basepath}/{out_basename}_pts.geojson", "w") as pts_out:
        json.dump(points, pts_out)

    with open(f"{out_basepath}/{out_basename}_polys.geojson", "w") as poly_out:
        json.dump(polys, poly_out)

    with open(f"{out_basepath}/{out_basename}_lines.geojson", "w") as lines_out:
        json.dump(lines, lines_out)

    with open(f"{out_basepath}/{out_basename}_tags.json", "w") as outtags:
        json.dump(tagging_rel, outtags)

if __name__ == "__main__":
    geojson_path = sys.argv[1]
    csv_path = sys.argv[2]
    parseJson(geojson_path,csv_path)