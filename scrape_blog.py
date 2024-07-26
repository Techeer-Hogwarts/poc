import requests
from bs4 import BeautifulSoup
import json
import time 

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

url = 'https://velog.io/@su_under/'
driver.get(url)

driver.implicitly_wait(100)
time.sleep(5)

html = driver.page_source
driver.quit()

# Use BeautifulSoup to parse the rendered HTML
soup = BeautifulSoup(html, 'html.parser')

body = soup.body.find_all('div', class_='FlatPostCard_block__a1qM7')
for i in body:
    tag_flag = False
    print("title: ", i.h2.text)
    tags = i.find_all('a')
    for tag in tags:
        if "TagItem_tagLink__Cga_K" in tag["class"]:
            print("tags: ", tag.text)
            tag_flag = True

    if not tag_flag:
        print("tags: None")
    print("=====================================\n")
