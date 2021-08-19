import pandas as pd
from bs4 import BeautifulSoup
import requests
import re
import multiprocessing as mp

links_df = pd.read_csv('C:/Users/shic/Desktop/shinhan_simon/google_drive/crawler_data/estate_news/article_links.csv')

header = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'
}

article_title    = []
article_contents = []

# 네이버 뉴스 웹페이지에서 제목, 본문, 언론사, 작성일자를 가져오는 함수입니다.
def get_article_data(url_now):
    
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
        else:
            return_dict['article_title'] = soup.find_all('h3',id='articleTitle')[0].text

        # 기사의 본문 가져오기
        if soup.find_all('div',id='articleBodyContents') == []:
            return_dict['article_content'] = 'no article contents'
        else:
            article_txt = soup.find_all('div',id='articleBodyContents')[0].text
            return_dict['article_content'] = re.sub('\n|\t|\r','',article_txt)

        # 기사의 작성 언론사 가져오기
        if soup.find_all('div',class_='press_logo') == []:
            return_dict['article_writer'] = 'no article writer'
        elif soup.find_all('div',class_='press_logo')[0].find_all(
                'img',src=re.compile('^https://mimgnews.pstatic.net/')) == []:
            return_dict['article_writer'] = 'no article writer'
        else:
            return_dict['article_writer'] = soup.find('div',class_='press_logo').find(
                'img',src=re.compile('^https://mimgnews.pstatic.net/'))['title']

        # 기사의 작성 일자시간 가져오기
        if soup.find_all('span',class_='t11') == []:
            return_dict['write_time'] = 'no write time'
        else:
            return_dict['write_time'] = soup.find_all('span',class_='t11')[0].text

        return return_dict

# 병렬처리를 한 뒤, 결과를 합쳐 저장합니다.
if __name__ == '__main__':
    pool = mp.Pool(mp.cpu_count())
    result = pool.map(get_article_data,links_df['links'])
    result_df = pd.DataFrame(result)
    result_df.to_csv('C:/Users/shic/Desktop/shinhan_simon/google_drive/crawler_data/estate_news/article_df.csv',index=0)

