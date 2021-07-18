import requests
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import json
import os

SHOW_FORMATS = [
    "TV",
    "TV_SHORT",
    "MOVIE",
    "SPECIAL",
    "OVA",
    "ONA",
    "MUSIC"
]

def pull_airing_data():
    #path of your chromedriver installation
    DRIVER_PATH = os.getenv('DRIVER_PATH')
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(executable_path=DRIVER_PATH,chrome_options=chrome_options)
    ## TODO: use time to decide which season we're currently in and modify url
    url ='https://anilist.co/search/anime?season=SUMMER'
    driver.get(url)
    html = driver.page_source

    SCROLL_PAUSE_TIME = 2

    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    #collect all anime from the loaded page
    anime_titles = driver.find_elements_by_class_name('title')
    anime_IDs = []
    for anime in anime_titles:
        #get the anilist IDs for all collected anime
        ID = anime.get_attribute('href').split("/")[4]
        anime_IDs.append(ID)
    #close the browser
    driver.quit()

    #populate JSON of anime data using IDs and anilist API queries
    anime_data = {}
    for format in SHOW_FORMATS:
        anime_data[format] = []
    for ID in anime_IDs:
        query = '''
        query ($id: Int) {
            Media(id: $id, type: ANIME) {
              title{
                romaji
              }
            	format
            isAdult
            }
        }
        '''
        variables = {
            'id': ID,
        }
        url = 'https://graphql.anilist.co'
        response = requests.post(url, json={'query': query, 'variables': variables})
        response = json.loads(response.text.encode('utf8'))
        format = response["data"]["Media"]["format"]
        anime_data[format].append(response)
    return anime_data
