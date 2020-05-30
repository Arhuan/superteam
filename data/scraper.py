import json
import pathlib
import requests
from bs4 import BeautifulSoup

stats_pages = [
    "https://www.basketball-reference.com/leagues/NBA_2019_per_game.html",
    "https://www.basketball-reference.com/leagues/NBA_2018_per_game.html",
    "https://www.basketball-reference.com/leagues/NBA_2017_per_game.html"
]

stats_years = [
    "stats-2019",
    "stats-2018",
    "stats-2017",
]

def save_html(html, path):
    with open(path, "wb") as f:
        f.write(html)

def open_html(path):
    with open(path, "rb") as f:
        return f.read()

def get_stats_data():
    for i, page in enumerate(stats_pages):
        path = pathlib.Path(f"{stats_years[i]}.html")

        if path.exists():
            continue

        r = requests.get(page)
        save_html(r.content, f"{stats_years[i]}.html") 

def parse_html(html):
    soup = BeautifulSoup(html, "html.parser")
   
    data = []
    rows = soup.select("tbody tr")

    for row in rows:
        if row.get("class")[0] == "thead":
            continue

        player = dict()

        player["name"] = row.select_one("td[data-stat='player'] a").text
        player["position"] = row.select_one("td[data-stat='pos']").text
        player["age"] = int(row.select_one("td[data-stat='age']").text)

        fg_per_game = float(row.select_one("td[data-stat='fg_per_g']").text)
        fga_per_game = float(row.select_one("td[data-stat='fga_per_g']").text)
        player["fg_percentage"] = fg_per_game / fga_per_game if (fga_per_game != 0.0) else None

        ft_per_game = float(row.select_one("td[data-stat='ft_per_g']").text) 
        fta_per_game = float(row.select_one("td[data-stat='fta_per_g']").text) 
        player["ft_percentage"] = ft_per_game / fta_per_game if (fta_per_game != 0.0) else None

        fg3_per_game = float(row.select_one("td[data-stat='fg3_per_g']").text)
        fg3a_per_game = float(row.select_one("td[data-stat='fg3a_per_g']").text)
        player["3pt_percentage"] = fg3_per_game / fg3a_per_game if (fg3a_per_game != 0.0) else None

        player["points"] = float(row.select_one("td[data-stat='pts_per_g']").text)
        player["rebounds"] = float(row.select_one("td[data-stat='orb_per_g']").text) + float(row.select_one("td[data-stat='drb_per_g']").text)
        player["assists"] = float(row.select_one("td[data-stat='ast_per_g']").text)
        player["steals"] = float(row.select_one("td[data-stat='stl_per_g']").text)
        player["blocks"] = float(row.select_one("td[data-stat='blk_per_g']").text)
        player["turnovers"] = float(row.select_one("td[data-stat='tov_per_g']").text)

        data.append(player)

    return data

def create_data_json():
    for stats in stats_years:
        with open(f"{stats}.json", "w") as f:
            data = parse_html(open_html(f"{stats}.html"))
            json.dump(data, f)

get_stats_data()
create_data_json()
