import json
import time

import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as wait
from webdriver_manager.chrome import ChromeDriverManager

# optionally specify categories, uncomment other line to include category
categories = ["Restaurants", "active", "All+Arts+%26+Entertainment", "Nightlife"]

# specify city/state pairs to scrape
# TODO: append state abbreviations
# cities = ["San Francisco Bay Area, CA", "San Francisco", "San Jose", "Oakland", "Berkeley", "Fremont", "Concord", "Palo Alto", "Hayward", "Santa Rosa", "Sunnyvale", "Vallejo", "Walnut Creek", "Mountain View", "Cupertino", "San Leandro", "Pleasanton", "Mill Valley", "Milpitas", "Fairfield", "Dublin", "Millbrae", "Daly City", "San Mateo", "East Palo Alto", "Menlo Park", "Morgan Hill", "Santa Clara", "Sausalito", "Atherton", "Belmont", "Antioch", "Livermore", "Pacifica", "Emeryville"]
cities = ["Austin, TX"]

# initialize empty list of urls to pickle
urls = []

# specifying chrome options
chromeOptions = webdriver.ChromeOptions()
chromeOptions.add_argument("start-maximized")
chromeOptions.add_argument("enable-automation")
# chromeOptions.add_argument("--headless")
chromeOptions.add_argument("--no-sandbox")
chromeOptions.add_argument("--disable-infobars")
chromeOptions.add_argument("--disable-dev-shm-usage")
chromeOptions.add_argument("--disable-browser-side-navigation")
chromeOptions.add_argument("--disable-gpu")

# initialize automated chrome scraper
driver = webdriver.Chrome(ChromeDriverManager().install(), options=chromeOptions)

# iterate through all categories, this one code block
for category in categories:
    if category == "All+Arts+%26+Entertainment":
        base_url = 'https://www.yelp.com/search?desc='+category
    else:
        base_url = 'https://www.yelp.com/search?cflt='+category
    for city in cities:
        url = base_url+'&find_loc='+city

        print(url)

        driver.get(url)
        result_locator = "//*[contains(text(), '1 of ')]"
        try:
    #         wait(driver, 5).until(EC.visibility_of_element_located(By.XPATH, result_locator))
            time.sleep(5)
            results = driver.find_element(by=By.XPATH, value=result_locator).text
            results = int(results[results.index('of')+3:])
            
            for i in range(0, results):
                urls.append(url+'&start='+str(i*10))
        except:
            results = 'oof does not exist most likely'
        print(results)

with open('yelp_urls.json', "w") as f:
    json.dump(urls, f)

driver.quit()
