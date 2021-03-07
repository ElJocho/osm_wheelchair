import json
import requests
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt

tag = "wheelchair=yes"
OHSOME_API = "https://api.ohsome.org/v1/"


def query(tags, bpolys: str, time: str = None, endpoint: str = None):
    """Query ohsome API endpoint."""

    url = OHSOME_API + endpoint

    data = {"bpolys": bpolys, "filter": tags, "time": time}
    response = requests.post(url, data=data)

    logger.info("Request data from API")
    logger.info("Endpoint = {}".format(url))
    logger.info("Query Filter: " + tags)

    try:
        response = requests.post(url, data=data)
        response.raise_for_status()
        response_text = response.text
    except requests.exceptions.HTTPError as http_err:
        print(f'HTTP error: {http_err}')
    except Exception as err:
        print(f'Error occurred: {err}')

    visualize_ohsome(response_text)


def visualize_ohsome(data, group_by=False):
    response_json = json.loads(data)

    json_key = list(response_json)[2]

    if group_by == True:
        results = response_json[json_key]
        df = pd.json_normalize(results, record_path='result', meta=['groupByObject'])
        df['timestamp'] = df['timestamp'].str.slice(stop=4)
        df = df[~df['groupByObject'].str.contains('remainder')]
        df.rename(columns={'groupByObject': 'Tag'}, inplace=True)
        ax1 = sns.lineplot(data=df, x="timestamp", y="value", hue='Tag')

    else:
        df = pd.json_normalize(response_json, record_path='result')
        df['timestamp'] = df['timestamp'].str.slice(stop=4)
        df.rename(columns={'result': 'Tag'}, inplace=True)
        ax1 = sns.lineplot(data=df, x="timestamp", y="value", legend="full",
                           label="Tagged objects")

    for line in ax1.lines:
        y = line.get_ydata()
        if len(y) > 0:
            ax1.annotate(f'{y[-1]:}', xy=(1, y[-1]), xycoords=('axes fraction', 'data'),
                         ha='left', va='center', color=line.get_color())

    sns.set_style("darkgrid")
    plt.show()