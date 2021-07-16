import pandas as pd
import numpy as np
from selenium import webdriver
import datetime
from bs4 import BeautifulSoup
import requests
import re
import multiprocessing as mp

date_list = []
today = datetime.datetime.today()

# 코드를 작성하고 있는 2021년 7월 15일 부터 2017년 1월 1일까지 date range.
for num_day in range(1,1657):
    tmp_date = today - datetime.timedelta(days = num_day)
    tmp_date = str(tmp_date).split(' ')[0].replace('-','.')
    date_list.append(tmp_date)

base_url = 'https://search.naver.com/search.naver?where=news&query=%EB%B6%80%EB%8F%99%EC%82%B0114&sm=tab_opt&sort=0&photo=0&field=0&pd=3&ds={}&de={}&start={}'

header = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

urls_list = []
for day in date_list:
    for num in [1,11,21]:
        urls_list.append(base_url.format(day,day,str(num)))

link_list = []
def get_url_with_date(urll):
    now_req    = requests.get(urll,headers=header).text
    now_search = BeautifulSoup(now_req,'html').find_all('div',class_='info_group')

    for parts in now_search:
        if parts.find_all('a',href=re.compile('^https://news.naver.com')):
            pass
        else:
            link_found = parts.find_all('a',href = re.compile('^https://news.naver.com'))[0]['href']
            link_list.append(link_found)

if __name__ == '__main__':
    pool = mp.Pool(mp.cpu_count())
    pool.map(get_url_with_date,urls_list)