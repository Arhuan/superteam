import pandas as pd
import json

def get_data():
    data = pd.read_json("./data/stats-2016.json")
    labels = pd.read_json("./data/fantasy-2016.json")

    print(data)
    print(labels)

if __name__ == "__main__":
    get_data()

