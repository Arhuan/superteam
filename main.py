import pandas as pd
import numpy as np
import json
from models import lin_reg

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
    """Retrieve training and validation data as a numpy array"""
    
    data_final = pd.DataFrame()
    labels_final = pd.DataFrame()

    for json in data_jsons:
        data = pd.read_json(json["stats"])
        labels = pd.read_json(json["fantasy"])

        data_final = data_final.append(data)
        labels_final = labels_final.append(labels)

    data_final, labels_final = clean_data(data_final, labels_final)
              
    return data_final.to_numpy(), labels_final.to_numpy()
        
def clean_data(data, labels):
    """Cleans up and rearranges the data and labels, returns data and label DataFrames

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

    model = lin_reg.LinearRegression(lammy=1)
    
    model.fit(X, y)

