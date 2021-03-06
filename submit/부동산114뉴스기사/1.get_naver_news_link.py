import pandas as pd
import datetime
from bs4 import BeautifulSoup
import requests
import re
import time
import multiprocessing as mp
import random
from multiprocessing import freeze_support

date_list = []
today = datetime.date(2021,8,1)

# 시간 차이를 구해서 기간의 날짜 수 만큼 range.
date_from_to = today - datetime.date(2012,1,1)
for num_day in range(1,(date_from_to.days)+1):
    tmp_date = today - datetime.timedelta(days = num_day)
    tmp_date = str(tmp_date).split(' ')[0].replace('-','.')
    date_list.append(tmp_date)

base_url = 'https://search.naver.com/search.naver?where=news&query=%EB%B6%80%EB%8F%99%EC%82%B0114&sm=tab_opt&sort=0&photo=0&field=0&pd=3&ds={}&de={}&start={}'

header = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# 날짜와 시작 페이지 번호를 조합해 최종 url 목록을 만듭니다.
urls_list = []
for day in date_list:
    for num in [1,11,21,31]:
        urls_list.append(base_url.format(day,day,str(num)))

# 네이버뉴스에서 부동산114로 검색하여 나온 뉴스기사들 중, 네이버 뉴스의 링크만을 가져옵니다.
def get_naver_news_url(urll):
    link_list = []
    
    if requests.get(urll,headers=header).status_code == 404:
        pass

    else:
        now_req    = requests.get(urll,headers=header)
        now_search = BeautifulSoup(now_req.text,'html.parser').find_all('div',class_='info_group')

        # 검색결과에서 기본적인 정보를 가진 info_group을 파싱합니다.
        for parts in now_search:

            # 파싱한 결과에 포함된 네이버 뉴스 링크를 가져옵니다.
            if parts.find_all('a',href=re.compile('news.naver.com')) == []:
                pass

            else:
                link_found = parts.find_all('a',href = re.compile('news.naver.com'))[0]['href']
                link_list.append(link_found)
            
    time.sleep(random.uniform(1,3))

    return link_list

if __name__ == '__main__':
    freeze_support()
    pool = mp.Pool(mp.cpu_count())
    result = pool.map(get_naver_news_url,urls_list)
    result_df = pd.DataFrame(sum(result,[]))
    result_df.columns = ['links']
    result_df.to_csv('C:/Users/shic/Desktop/shinhan_simon/google_drive/crawler_data/estate_news/article_links.csv',index=0)
    # 9.39
