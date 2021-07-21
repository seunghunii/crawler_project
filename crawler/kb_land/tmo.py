import pandas as pd
from selenium import webdriver
import numpy as np
from bs4 import BeautifulSoup
import re
import requests
from time import sleep
import json

# basic params
dir_for_shinhan = 'C:/Users/shic/Desktop/shinhan_simon/chromedriver/chromedriver.exe'
dir_for_seunghun = 'C:/Users/rsh15/Desktop/seunghuni/selenium/chromedriver.exe'

header = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# region code
region_data = pd.read_csv('C:/Users/rsh15/Desktop/seunghuni/crawler_project/data_save/kb_land/region_code.csv')
region_data = region_data[region_data['small_region_name']!='(전체)']
region_data['big_region_code'] = region_data['big_region_code'].astype(int)
region_data['small_region_code'] = region_data['small_region_code'].astype(int)
region_code = region_data[region_data['big_region_name'].isin(['서울','경기','인천'])]

# make date list([year,month])
date_list = []
for year in range(2010,2022):
    year = str(year)
    for month in range(1,13):
        if int(month) < 10:
            month = '0' + str(month)
        else:
            month = str(month)

        if year == '2021' and month == '07':
            break

        date_list.append([year,month])

base_url = 'https://onland.kbstar.com/quics?page=C060737&%EB%B2%95%EC%A0%95%EB%8F%99%EB%8C%80%EC%A7%80%EC%97%AD%EC%BD%94%EB%93%9C={}&%EB%B2%95%EC%A0%95%EB%8F%99%EC%A4%91%EC%A7%80%EC%97%AD%EC%BD%94%EB%93%9C={}&%EA%B8%B0%EC%A4%80%EB%85%84={}&%EA%B8%B0%EC%A4%80%EC%9B%94={}&QSL=F'

def kb_land_crawler(date_list):
    year  = date_list[0]
    month = date_list[1]

    for region in region_code.iterrows():
        tmp_url = base_url.format(int(region[1]['big_region_code']),  # 대지역코드
                                  int(region[1]['small_region_code']),  # 중지역코드
                                  year, month)

        # URL 접속
        tmp_req = requests.get(tmp_url, headers=header)

        ret_a = re.search("var graphYn1 = [$](.+?);", tmp_req.text, re.S).group(1)
        ret_a = ret_a.replace(".trim('[", "").replace("') == '' ? false: true", "").replace('Date.UTC(', '')
        ret_a.split('], [')

        date_list_aa = []
        data_list_aa = []

        for k in ret_a:
            tmpp = k.split('),')
            data_wrangle = tmpp[0].split(', ')
            #data_wrangle[1] = str(int(data_wrangle[1]) + 1)

            #date_list_aa.append(','.join(data_wrangle))
            #data_list_aa.append(float(tmpp[1].replace(']', '')))

        return data_wrangle

print(kb_land_crawler(date_list[0]))
