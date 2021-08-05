import pandas as pd
from selenium import webdriver
import numpy as np
from bs4 import BeautifulSoup
import re
import requests
from time import sleep
import json
import multiprocessing as mp
from multiprocessing import freeze_support

# basic params
dir_for_shinhan = 'C:/Users/shic/Desktop/shinhan_simon/chromedriver/chromedriver.exe'
dir_for_seunghun = 'C:/Users/rsh15/Desktop/seunghuni/selenium/chromedriver.exe'

header = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

crawler_shinhan = 'C:/Users/shic/Desktop/crawler_project/'
crawler_seunghun = 'C:/Users/rsh15/Desktop/seunghuni/crawler_project/'

# region code
region_data = pd.read_csv(crawler_seunghun + 'data_save/kb_land/region_code.csv',
                          dtype = {'big_region_code' : str,
                                   'big_region_name' : str,
                                   'small_region_code' : str,
                                   'small_region_name' : str})

# make date list([year,month])
date_list = []
for year in range(2012,2022):
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

def kb_land_crawler(dates):
    year  = dates[0]
    month = dates[1]

    df_list = []
    for region in region_data.iterrows():
        tmp_url = base_url.format(region[1]['big_region_code'],  # 대지역코드
                                  region[1]['small_region_code'],  # 중지역코드
                                  year, month)

        # URL 접속
        tmp_req = requests.get(tmp_url, headers=header)

        return_df = pd.DataFrame({
            'year'    : year,
            'month'   : month,
            'region_b': region[1]['big_region_name'],
            'region_s': region[1]['small_region_name'],
            'req_text': tmp_req.text
        },index=[0])

        df_list.append(return_df)

    return pd.concat(df_list,axis=0)
    
if __name__ == '__main__':
    freeze_support()
    pool = mp.Pool(mp.cpu_count())
    result = pool.map(kb_land_crawler,date_list)
    result_df = pd.concat(result,axis=0)
    result_df.to_csv(crawler_seunghun + 'data_save/kb_land/kb_land_req_text.csv',index=0)
