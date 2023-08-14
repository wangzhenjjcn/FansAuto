import requests
from bs4 import BeautifulSoup
from PIL import Image
import pytesseract
import json
from io import BytesIO
import re
import time
import csv


def get_last_movies():
    url = "https://www.yinfans.me/"
    payload = {}
    headers = {
    'DNT': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    # 使用正则表达式匹配链接
    pattern = r"https://www\.yinfans\.me/movie/[^\s\"<>'\(\)]+"
    return re.findall(pattern, response.text)
    

def get_download_links(page_url):
    payload = {}
    headers = {
    'DNT': '1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7'
    }

    response = requests.request("GET", page_url, headers=headers, data=payload)
    new_soup = BeautifulSoup(response.text, 'html.parser')

    tab_content_data = []
    tab_content_div = new_soup.find('div', class_='tab-content')
    if tab_content_div==None:
        return tab_content_data
    for td in tab_content_div.find_all('td'):
        text = td.get_text()
        links=[]
        for a_tag in td.find_all('a', href=True):
            if a_tag['href'].startswith("magnet:?"):
                links.append(a_tag['href'])
        if links:  
            for link in links:
                tab_content_data.append((text, link))
    print(tab_content_data)
    return tab_content_data


def get_imdblink(page_url):
    payload = {}
    headers = {
    'DNT': '1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7'
    }

    response = requests.request("GET", page_url, headers=headers, data=payload)
    soup = BeautifulSoup(response.text, 'html.parser')
    content_div = soup.find('div', id='content')
    if content_div:
        for text in content_div.stripped_strings:
            if text.startswith("https://www.imdb.com/title/"):
                first_imdb_text_match = text
                return first_imdb_text_match



def get_imdbId(page_url):
    payload = {}
    headers = {
    'DNT': '1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7'
    }

    response = requests.request("GET", page_url, headers=headers, data=payload)
    soup = BeautifulSoup(response.text, 'html.parser')
    content_div = soup.find('div', id='content')
    if content_div:
        for text in content_div.stripped_strings:
            if text.startswith("https://www.imdb.com/title/"):
                first_imdb_text_match = text
                imdbid=first_imdb_text_match.replace("https://www.imdb.com/title/","").replace("/","")
                if imdbid==None:
                    return 0
                return imdbid


if __name__ == "__main__":
    dataFile="data.csv"
    urls=get_last_movies()
    for url in urls:
        links=get_download_links(url)
        datafilename=str(url).replace('https://www.yinfans.me/movie/',"")+"-"+str(get_imdbId(url))+".txt"
        with open(datafilename, "w", encoding="utf-8", newline="") as datafile:
            datafile.write(str(url).replace('https://www.yinfans.me/movie/',"")+":"+str(links))
