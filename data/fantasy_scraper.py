import json
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from unidecode import unidecode

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
    driver.implicitly_wait(10)
    
    try:
        for i, page in enumerate(pages):
            with open(f"{fantasy_filenames[i]}.json", "w") as f:
                driver.get(page)
                
                driver.find_element_by_xpath("//a[@ng-click='SetPageSize(300);']").click()
                wait_for_table_data(driver)
                hide_popups(driver)
                load_all_rows(driver)

                # TODO: bit of a hack, revisit and fix later
                wait_for_table_data(driver)

                data = parse_html(driver.page_source)
                json.dump(data, f)
    finally:
        driver.quit()

def hide_popups(driver):
    try:
        driver.find_element_by_xpath("//button[@class='fs-close-button']").click()
    except:
        print("Ad popup not visible")
    try:
        driver.find_element_by_xpath("//div[@class='cookieinfo-close']").click()
    except:
        print("Cookies popup not visible")

def wait_for_table_data(driver):
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_all_elements_located((By.XPATH, "//td")))

def load_all_rows(driver):
    # TODO: implement a function that checks to see if the table has loaded all possible new data so we can exit earlier
    for i in range(3):
        load_more_button = driver.find_element_by_xpath("//div[@ng-app='fantasydata']//a[@ng-hide='LoadingMore']")

        actions = ActionChains(driver)
        actions.move_to_element(load_more_button).click(load_more_button).perform()

        wait_for_table_data(driver)

def parse_html(html):
    soup = BeautifulSoup(html, "html.parser")

    data = []

    rows = soup.select("div[class='k-grid-content-locked'] tbody tr")

    for row in rows:
        player = dict()

        player["rank"] = int(row.select_one("span[ng-bind='dataItem.Rank']").text)
        player["name"] = re.sub(r"\W+", "",  unidecode(row.select_one("a").text)).lower()
        
        print(player)

        data.append(player)

    return data

def main():
    get_data(fantasy_pages, fantasy_filenames)

if __name__ == "__main__":
    main()
