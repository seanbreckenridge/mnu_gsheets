# grab links from the MAL club to attach to mnu ids
# need to use selenium here since external links arent scrapable

import json
from jikanpy import Jikan
from time import sleep
from selenium import webdriver

j = Jikan("http://localhost:8000/v3/")
relations = j.club(72940)["anime_relations"]


# get credentials from file
with open("credentials.json", "r") as f:
    creds = json.load(f)
    username, password = creds["username"], creds["password"]


# create webdriver
driver = webdriver.Chrome()


# Login
driver.get("https://myanimelist.net/login.php")
# driver.find_element_by_css_selector(".modal-container button").click()  # accept privacy policy changes for this session
driver.find_element_by_id("loginUserName").send_keys(username)
driver.find_element_by_id("login-password").send_keys(password)
driver.find_element_by_css_selector(
    ".inputButton.btn-form-submit[value='Login']"
).click()

# wait for login?? shouldnt POST do this?
sleep(10)

url_info = {}

for page_info in relations:
    url: str = "https://myanimelist.net/anime/{}".format(page_info["mal_id"])
    driver.get(url)
    el = driver.find_element_by_css_selector(
        "#content > table > tbody > tr > td.borderClass > div > div.pb16 > a"
    )
    if el is None:
        print(f"Couldnt find ID for {url}")
    else:
        url_info = {url: el.get_attribute("href")}
        print(el.get_attribute("href"))
    sleep(5)

with open("results.json", "w") as f:
    f.write(json.dumps(url_info))
