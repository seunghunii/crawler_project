import pandas as pd
import requests
from glob import glob
import multiprocessing as mp

header = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

code_data_list = glob('C:/Users/shic/Desktop/crawler_project/data_save/stock_price/*.csv')
kosdaq = pd.read_csv(code_data_list[0],encoding='CP949')
kospi  = pd.read_csv(code_data_list[1],encoding='CP949')

# 네이버주식 URL에 종목 코드와 page number를 반복해가면서 kospi, kosdaq url 생성.
urls_list_kosdaq = []
for kosdaq_rows in kosdaq.iterrows():
    for page_num in range(1,250):
        code = kosdaq_rows[1]['종목코드']
        bind_url = 'https://finance.naver.com/item/sise_day.nhn?code=' + code + '&page=' + str(page_num)
        urls_list_kosdaq.append([code,'kosdaq',bind_url])

urls_list_kospi = []
for kospi_rows in kospi.iterrows():
    for page_num in range(1,250):
        code = kospi_rows[1]['종목코드']
        bind_url = 'https://finance.naver.com/item/sise_day.nhn?code=' + code + '&page=' + str(page_num)
        urls_list_kospi.append([code,'kospi',bind_url])

urls_list_bind = urls_list_kosdaq + urls_list_kospi

def get_stock_df_with_url(url_iter):
    reqq = requests.get(url_iter[2],headers=header)

    stock_df = pd.read_html(reqq.text)[0]
    stock_df['code'] = url_iter[0]
    stock_df['type'] = url_iter[1]

    return stock_df

if __name__ == '__main__':
    mp.freeze_support()
    pool = mp.Pool(mp.cpu_count())
    result = pool.map(get_stock_df_with_url,urls_list_bind)
    result_df = pd.concat(result,axis=0)
    result_df.to_csv('C:/Users/shic/Desktop/crawler_project/data_save/stock_price/stock_price_record.csv',index=False)

