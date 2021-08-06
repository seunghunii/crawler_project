import pandas as pd
import numpy as np
from selenium import webdriver
import datetime
from bs4 import BeautifulSoup
import requests
import re
import multiprocessing as mp

links_df = pd.read_csv('C:/Users/shic/Desktop/shinhan_simon/google_drive/crawler_data/estate_news/article_links.csv')

base_url = 'https://search.naver.com/search.naver?where=news&query=%EB%B6%80%EB%8F%99%EC%82%B0114&sm=tab_opt&sort=0&photo=0&field=0&pd=3&ds={}&de={}&start={}'
header = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

article_title    = []
article_contents = []

def estate_news_crawler(url_now):
    
    return_dict = {}
    soup = BeautifulSoup(requests.get(url_now,headers=header).text,'html.parser')

    if soup.status_code == 404:
        pass
    else:
        for soup_rm in soup.find_all('strong',class_='median_and_summary'):
            soup_rm.decompose()

        # 기사의 제목 가져오기
        if soup.find_all('h3',id='articleTitle') == []:
            return_dict['article_title'] = 'no article title'
            #article_title.append('no article title')
        else:
            return_dict['article_title'] = soup.find_all('h3',id='articleTitle')[0].text
            #article_title.append(soup.find_all('h3',id='articleTitle')[0].text)

        # 기사의 본문 가져오기
        if soup.find_all('div',id='articleBodyContents') == []:
            return_dict['article_content'] = 'no article contents'
            #article_contents.append('no article contents')
        else:
            return_dict['article_content'] = soup.find_all('div',id='articleBodyContents')[0].text
            #article_contents.append(soup.find_all('div',id='articleBodyContents')[0].text)

        # 기사의 작성 언론사 가져오기
        if soup.find_all('div',class_='article_header')[0].find_all('img',src=re.compile('.png$')) == []:
            return_dict['article_writer'] = 'no article writer'
        else:
            return_dict['article_writer'] = soup.find('div',class_='article_header').find('img',src=re.compile('.png$'))['title']

        # 기사의 작성 일자시간 가져오기
        if soup.find_all('span',class_='t11') == []:
            return_dict['write_time'] = 'no write time'
        else:
            return_dict['write_time'] = soup.find_all('span',class_='t11')[0].text

        return return_dict

if __name__ == '__main__':
    pool = mp.Pool(mp.cpu_count())
    result = pool.map(estate_news_crawler,links_df['links'])
    result_df = pd.DataFrame(result)
    result_df.to_csv('C:/Users/shic/Desktop/shinhan_simon/google_drive/crawler_data/estate_news/article_df2.csv',index=0)

