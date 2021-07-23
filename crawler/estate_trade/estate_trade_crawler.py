import multiprocessing as mp
import pandas as pd
import numpy as np
from selenium import webdriver
from bs4 import BeautifulSoup
import re

dir_for_shinhan = 'C:/Users/shic/Desktop/shinhan_simon/chromedriver/chromedriver.exe'
dir_for_seunghun = 'C:/Users/rsh15/Desktop/seunghuni/selenium/chromedriver.exe'

class Parser():
    def __init__(self):
        self.pool = mp.Pool(processes = mp.cpu_count())

    def main_crawler(self,tmp_url):
        driver = webdriver.Chrome(dir_for_shinhan)
        driver.get(tmp_url)

        soup = BeautifulSoup(driver.page_source,'xml')
        total_row = soup.find('totalCount').text

        if total_row == '0':
            pass

        return_list = []
        for soup_parser in soup.find_all('item'):
            data_parser = re.sub('\<(.*?)\>',' ',str(soup_parser))
            data_parser = re.sub('\s{2,}',' ',data_parser).strip().split(' ')

            if len(data_parser) == 24:
                data_parser = data_parser + ['0','0']

            add_df = pd.DataFrame(
                dict(zip(data_parser))
            )

            return_list.append(add_df)

        return pd.concat(return_list,axis=0)

    def multi_processing(self,urls_list):
        self.pool.map(self.main_crawler,urls_list)

