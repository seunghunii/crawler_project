import multiprocessing as mp
import pandas as pd
import numpy as np
from selenium import webdriver
from bs4 import BeautifulSoup
import re

dir_for_shinhan = 'C:/Users/shic/Desktop/shinhan_simon/chromedriver/chromedriver.exe'
dir_for_seunghun = 'C:/Users/rsh15/Desktop/seunghuni/selenium/chromedriver.exe'

tagg = [ '거래금액','건축년도','년','도로명','도로명건물본번호코드','도로명건물부번호코드',
         '도로명시군구코드','도로명일련번호코드','도로명지상지하코드','도로명코드','법정동','법정동본번코드',
         '법정동부번코드','법정동시군구코드','법정동읍면동코드','법정동지번코드','아파트',
         '월','일','일련번호','전용면적','지번','지역코드','층','해제사유발생일','해제여부']

base_url = 'http://openapi.molit.go.kr/OpenAPI_ToolInstallPackage/service/rest/RTMSOBJSvc/getRTMSDataSvcAptTradeDev?serviceKey=OSuNRoNLvTbcIjbHj3pWw2WHibEa%2FhYBmhMnXocnaw6O%2Bg36NybrbO5jp38r%2BI646%2Fk9NLJoIVHRPWyKz%2Foiow%3D%3D&pageNo=1&numOfRows=10000&LAWD_CD={}&DEAL_YMD={}'

region_code = pd.read_csv('C:/Users/shic/Desktop/crawler_project/data_save/estate_trade/region_code_parsed.csv')
region_code = region_code[region_code['폐지여부'] != '폐지']

date_list = []
for year in range(2010,2022):
    for month in range(1,13):
        if year == 2021 and month == 7:
            break
        
        if len(str(month)) == 1:
            date_string = str(year) + '0' + str(month)
        else:
            date_string = str(year) + str(month)
        
        date_list.append(date_string)

urls_list = []
for date in date_list:
    for region in region_code['법정동코드_cut']:
        urls_list.append(base_url.format(region,date))

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
                dict(zip(tagg,data_parser))
            )

            return_list.append(add_df)

        return pd.concat(return_list,axis=0)

    def multi_processing(self,urls):
        self.pool.map(self.main_crawler,urls)

parser = Parser()
result = parser.multi_processing(urls_list[0:100])
print(result)
