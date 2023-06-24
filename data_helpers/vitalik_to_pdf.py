import os

import pdfkit
import requests
from bs4 import BeautifulSoup

start_url = "https://vitalik.ca/"
folder_to_save = "data/vitalik_articles/"

response = requests.get(start_url)

soup = BeautifulSoup(response.text, "html.parser")
links = soup.find_all("a")

if not os.path.exists(folder_to_save):
    os.makedirs(folder_to_save)

for link in links:
    url = link.get("href")
    # to avoid visiting external links
    if url and (url.startswith("./") or url.startswith("/")):
        url = start_url + url.lstrip("/")
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        title = soup.title.string if soup.title else url
        file_name = f'{folder_to_save}{title.replace(" ", "_").replace("/", "_")}.pdf'
        try:
            # print(url, file_name)
            pdfkit.from_url(url, file_name)
            print(f"Saved {url} as {file_name}")
        except Exception as e:
            # pass
            print(f"Could not save {url} due to {e}")
