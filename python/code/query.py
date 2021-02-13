import json 
import requests
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt



# bpolys = """
# {
#   "type": "FeatureCollection",
#   "features": [
#     {
#       "type": "Feature",
#       "properties": {},
#       "geometry": {
#         "type": "Polygon",
#         "coordinates": [
#           [
#             [
#               8.696022033691406,
#               49.43978020400602
#             ],
#             [
#               8.668212890625,
#               49.43866396851723
#             ],
#             [
#               8.634395599365234,
#               49.440896414087646
#             ],
#             [
#               8.622207641601562,
#               49.435984899682005
#             ],
#             [
#               8.62701416015625,
#               49.42135906938539
#             ],
#             [
#               8.645381927490234,
#               49.40985630864901
#             ],
#             [
#               8.661518096923828,
#               49.39835085202889
#             ],
#             [
#               8.656196594238281,
#               49.38661921339738
#             ],
#             [
#               8.64349365234375,
#               49.37991416188827
#             ],
#             [
#               8.654136657714844,
#               49.36683667977814
#             ],
#             [
#               8.66872787475586,
#               49.35822823332857
#             ],
#             [
#               8.707695007324219,
#               49.35834004099321
#             ],
#             [
#               8.730010986328125,
#               49.365048035722864
#             ],
#             [
#               8.755416870117188,
#               49.388183593767955
#             ],
#             [
#               8.789405822753906,
#               49.405723590823364
#             ],
#             [
#               8.779449462890625,
#               49.426941961888886
#             ],
#             [
#               8.757648468017578,
#               49.44033831222273
#             ],
#             [
#               8.696022033691406,
#               49.43978020400602
#             ]
#           ]
#         ]
#       }
#     }
#   ]
# }
# """

# OHSOME_API="https://api.ohsome.org/v1/"
# endpoint = "elements/count"
# start_time = "2010-01-01"
# end_time = "2021-02-01" 
# interval="P1Y"
# tags = "amenity=museum"


def get_geometries(tags, bpolys: str, start_time: str = None, end_time: str = None):

    tags = tags + " and wheelchair=yes or wheelchair=no or wheelchair=limited"

    timeframe=f"{start_time},{end_time}"

    url = OHSOME_API + "elements/centroid"
    data = {"bpolys": bpolys, "filter": tags, "time": timeframe, "properties":"tags"}

    try:
        response = requests.post(url, data=data)
#        response.raise_for_status()
        response_text = response.text
        response_json = json.loads(response_text)
    except requests.exceptions.HTTPError as http_err:
        print(f'HTTP error: {http_err}')
    except Exception as err:
        print(f'Error occurred: {err}')

    return (response_json)
    # with open('../../data/centroids.geojson', 'w') as f:
    #     json.dump(response_json, f)
    

def get_metadata(tags, bpolys: str, start_time: str = None, end_time: str = None, endpoint: str = None, interval: str = None) -> dict:
    """Query ohsome API endpoint with filter."""
    
    tags = tags + " and wheelchair=yes or wheelchair=no or wheelchair=limited"

    if not interval:
        interval = "P1Y"
    # timeframe=f"{start_time}/{end_time}/{interval}"
    timeframe=f"{start_time}/{end_time}/{interval}"

    url = OHSOME_API + "elements/count"
    data = {"bpolys": bpolys, "filter": tags, "time": timeframe}
    response = requests.post(url, data=data)

    try:
        response = requests.post(url, data=data)
        response_text = response.text
        response_json = json.loads(response_text)
    except requests.exceptions.HTTPError as http_err:
        print(f'HTTP error: {http_err}')
    except Exception as err:
        print(f'Error occurred: {err}')

    # get first tag from input as key for JSON 
    json_keyname = tags.partition("=")[0]
    to_kv_pair(response_json,json_keyname)


def to_kv_pair(response_json,json_keyname):
    "Ohsome JSON to key:value pair JSON"

    df = pd.json_normalize(response_json, record_path='result')
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df["dt_literal"] = df["timestamp"].values.astype("int")
    df["dt_literal"] = df["dt_literal"].div(1000000)

    kv_dict = dict(zip(df['dt_literal'], df['value']))
    kv_dict = {json_keyname:kv_dict}

    with open(f'../../data/{json_keyname}.geojson', 'w') as f:
        json.dumps(kv_dict, f)


def visualize_ohsome(response_text,group_by=False):
    
    response_json = json.loads(response_text)

    json_key = list(response_json)[2]

    if group_by==True:    
        results = response_json[json_key]
        df = pd.json_normalize(results, record_path='result', meta=['groupByObject'])
        df['timestamp'] = df['timestamp'].str.slice(stop=4)
        df = df[~df['groupByObject'].str.contains('remainder')]
        df.rename(columns={'groupByObject':'Tag'}, inplace=True)
        ax1 = sns.lineplot(data=df, x="timestamp", y="value", hue='Tag')
        
    else:
        df = pd.json_normalize(response_json, record_path='result')
        df['timestamp'] = df['timestamp'].str.slice(stop=4)
        df.rename(columns={'result':'Tag'}, inplace=True)
        ax1 = sns.lineplot(data=df, x="timestamp", y="value", legend="full",label="Tagged objects")
            
    for line in ax1.lines:
        y = line.get_ydata()
        if len(y)>0:
            ax1.annotate(f'{y[-1]:}', xy=(1,y[-1]), xycoords=('axes fraction', 'data'), 
                        ha='left', va='center', color=line.get_color())
    
    sns.set_style("darkgrid")    
    plt.show()


#get_geometries(tags,bpolys,start_time,end_time,interval)
#get_metadata(tags,bpolys,start_time,end_time)