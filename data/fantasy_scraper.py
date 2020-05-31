from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

DRIVER_PATH = "/usr/local/share/chromedriver"

fantasy_pages = [
    "https://fantasydata.com/nba/fantasy-basketball-leaders?scope=1&season=2019&seasontype=1&conference=1&date=03-11-2020",
    "https://fantasydata.com/nba/fantasy-basketball-leaders?scope=1&season=2018&seasontype=1&conference=1&date=03-11-2020",
    "https://fantasydata.com/nba/fantasy-basketball-leaders?scope=1&season=2017&seasontype=1&conference=1&date=03-11-2020",
    "https://fantasydata.com/nba/fantasy-basketball-leaders?scope=1&season=2016&seasontype=1&conference=1&date=03-11-2020"
]

fantasy_filenames = [
    "fantasy-2019",
    "fantasy-2018",
    "fantasy-2017",
    "fantasy-2016"
]

def get_data(pages, filenames):
    options = Options()
    driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)

    for page in pages:
        driver.get(page)

        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_all_elements_located((By.XPATH, "//td")))

        parse_html(driver.page_source)

    driver.quit()

def parse_html(html):
    soup = BeautifulSoup(html, "html.parser")

    data = []

    rows = soup.select("div[class='k-grid-content-locked'] tbody tr")

    for row in rows:
        player = dict()

        player["name"] = int(row.select_one("span[ng-bind='dataItem.Rank']").text)
        player["rank"] = row.select_one("a").text
        print(player)
        data.append(player)

    return data

def main():
    get_data(fantasy_pages, fantasy_filenames)

if __name__ == "__main__":
    main()
