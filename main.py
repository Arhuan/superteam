import pandas as pd
import numpy as np
import json

def get_data():
    data = pd.read_json("./data/stats-2016.json")
    labels = pd.read_json("./data/fantasy-2016.json")

    print(data)
    print(labels)

    labels = clean_labels(data, labels)

    print(labels)

def clean_labels(data, labels):
    """Prunes labels that do not have a matching player in data"""

    players = set(data["name"].tolist())

    return labels[labels['name'].isin(players)]

if __name__ == "__main__":
    get_data()

