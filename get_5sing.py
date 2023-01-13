"""
Created on 2023-1-13
@author: tsz
"""
import re
import os
import sys
import requests
import urllib.request as req
import json
from selenium import webdriver

_5sing_patstr = r'https:\/\/[^\<\>]*?\.mp3'
CONFIG_PATH = 'config.json'


def get_source_by_url(url:str):
    page = req.urlopen(url)
    htmlSrc = page.read()
    return htmlSrc.decode()

def get_source_by_url_ex(url:str):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36')
    chrome = webdriver.Chrome(options=options)
    chrome.get(url)
    return chrome.page_source

def web_file_down(patstr, url, path):
    htmlStr = get_source_by_url_ex(url)
    pat = re.compile(patstr)
    urlList = re.findall(pat, htmlStr)
    if len(urlList) == 0:
        print('file Not Found!\n')
        print(htmlStr)
        return

    if not os.path.exists(path):
        os.makedirs(path)
    file = requests.get(urlList[0])
    filename = get_filename_by_link(urlList[0])
    with open(os.path.join(path, filename), 'wb') as code:
        code.write(file.content)


def _5sing_file_down(url, path):
    web_file_down(_5sing_patstr, url, path)


def get_filename_by_link(fileurl: str):
    return fileurl.split('/')[-1]


def get_config(jsonfile):
    with open(jsonfile, 'r') as f:
        cfg = json.loads(f)
    return cfg


if __name__ == "__main__":
    if os.path.isfile(CONFIG_PATH):
        cfg = get_config(CONFIG_PATH)
        path = cfg['path']
    else:
        path = os.getcwd()
    if len(sys.argv) == 1:
        url = input('Enter Url:\n')
        _5sing_file_down(url, path)
    else:
        for url in sys.argv[1:]:
            try:
                _5sing_file_down(url, path)
            except Exception as err:
                print(err)
