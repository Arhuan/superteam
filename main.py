import pandas as pd
import numpy as np
import json

data_jsons = [
    {
        "stats": "./data/stats-2019.json",
        "fantasy": "./data/fantasy-2019.json"
    },
    {
        "stats": "./data/stats-2018.json",
        "fantasy": "./data/fantasy-2018.json"
    },
    {
        "stats": "./data/stats-2017.json",
        "fantasy": "./data/fantasy-2017.json"
    },
    {
        "stats": "./data/stats-2016.json",
        "fantasy": "./data/fantasy-2016.json"
    }
]

def get_data():
    for json in data_jsons:
        data = pd.read_json(json["stats"])
        labels = pd.read_json(json["fantasy"])

        data, labels = clean_data(data, labels)
        
def clean_data(data, labels):
    """Remove rows that do not have a corresponding matching data/label row"""
        
    data_players = set(data["name"].tolist())
    label_players = set(labels["name"].tolist())

    return data[data["name"].isin(label_players)], labels[labels["name"].isin(data_players)]

if __name__ == "__main__":
    get_data()

