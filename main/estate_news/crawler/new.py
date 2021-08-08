import requests
import pandas as pd
import datetime
from bs4 import BeautifulSoup
import re
import time
from random import uniform
import multiprocessing as mp
from multiprocessing import freeze_support


today = datetime.date(2021,7,31)
date_from_to = today - datetime.date(2012,1,1)

header = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'
}

date_list = []
for num_day in range(1,(date_from_to.days)+1):
    tmp_date = today - datetime.timedelta(days = num_day)
    tmp_date = str(tmp_date).replace('-','')
    date_list.append(tmp_date)

urll = 'https://news.naver.com/main/list.naver?mode=LS2D&sid2=260&mid=shm&sid1=101&date={}&page={}'

def get_links(date):
    return_dict = {}
    for pp in range(1,11):
        if pp == 5:
            time.sleep(uniform(1,3))

        tmp_url = urll.format(date,pp)

        reqq = requests.get(tmp_url,headers=header)

        time.sleep(uniform(0,1))

        soup = BeautifulSoup(reqq.text, 'html.parser')

        soup_main_content = soup.find('div',id='main_content')
        if soup_main_content == '':
            pass
        else:
            find_link = soup_main_content.find_all('a',href=re.compile('^https://news.naver.com/main/read.naver?'))
            for fl in find_link:
                return_dict['links'] = fl['href']

        return return_dict

if __name__ == '__main__':
    freeze_support()
    pool = mp.Pool(mp.cpu_count())
    result = pool.map(get_links,date_list)
    result_df = pd.DataFrame(result)
    result_df.columns = ['links']
    result_df.to_csv('C:/Users/rsh15/Google Drive/crawler_data/estate_news/new/naver_news_article_links.csv',index=0)
