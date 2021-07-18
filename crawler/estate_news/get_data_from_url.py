import pandas as pd
import numpy as np
from selenium import webdriver
import datetime
from bs4 import BeautifulSoup
import requests
import re
import multiprocessing as mp

links_df = pd.read_csv('C:/Users/shic/Desktop/crawler_project/data_save/estate_news/links_df.csv')
links_list = links_df[['links']]

header = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

article_title = []
article_contents = []

def estate_news_cralwer(link):
    soup = BeautifulSoup(requests.get(link,headers=header).text,'html.parser')

    for soup_rm in soup.find_all('strong',class_='median_and_summary'):
        soup_rm.decompose()

    if soup.find_all('h3',id='articleTitle') == []:
        article_title.append('no article title')
    else:
        article_title.append(soup.find_all('h3',id='articleTitle')[0].text)

    if soup.find_all('div',id='articleBodyContents') == []:
        article_contents.append('no article contents')
    else:
        article_contents.append(soup.find_all('div',id='articleBodyContents')[0].text)


if __name__ == "__main__":
    pool = mp.Pool(mp.cpu_count())
    pool.map(estate_news_cralwer,links_list)

print('sdt')