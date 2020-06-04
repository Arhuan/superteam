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
        
        return data.to_numpy(), labels.to_numpy()
        
def clean_data(data, labels):
    """Cleans up and rearranges the data and labels

    * Remove rows that do not have a corresponding matching data/label row
    * Match each row in data to each row in labels
    * Removes the names from the labels once they are matched with the proper row in data
    """
        
    data_players = set(data["name"].tolist())
    label_players = set(labels["name"].tolist())
    
    pruned_data = data[data["name"].isin(label_players)]
    pruned_labels = labels[labels["name"].isin(data_players)]
    
    sorted_data = pruned_data.sort_values(by=["name"]).reset_index(drop=True)
    sorted_labels = pruned_labels.sort_values(by=["name"]).reset_index(drop=True)
    
    return sorted_data, sorted_labels.drop(columns=["name"])

if __name__ == "__main__":
    X, y = get_data()

