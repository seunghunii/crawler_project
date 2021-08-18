import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import json
from random import uniform
import time

urll = 'https://data.iros.go.kr/cr/rs/selectRgsCsTab.do'

headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
    'Connection': 'keep-alive',
    'Content-Length': '151',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Cookie': 'WMONID=VdzGSVmMDjU; stoken=Vy3zFySFx5FAS1zTyGIDx5FDEMO1zCy1629212191zPy86400zAy33zEyXshPwJiufQjx78uqKWSB99x7A70EbrDx78ZeUo1cM63aDYQ3eOiKcPEtj2bMVudHF1O3Tx78x2BcKx2FBmfPx2FcpWJlx2B9DRPtFgx3Dx3DzKyUFSx796x79tjLx2FQNb9ht9FM1582XSHYx2FfvjNHuVShcgZfHhQWWnOnSIYgEH71x2F2jQ1x7ArzSSy00003097071zUURy480e8c733be2bbc22b3fba072a3941dbzMyXR0P1SScDQox3Dz; JSESSIONID=VMsOwjDn06iu1xwFH3Er4F66DfWn3u3n0z2aYyPgawy1t3TTpe59mlXlm24HbAaC.RF9vdXRfZG9tYWluMS9nNDQwTTE=',
    'Host': 'data.iros.go.kr',
    'Origin': 'https://data.iros.go.kr',
    'Referer': 'https://data.iros.go.kr/cr/rs/selectRgsCsDetl.do',
    'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
    'sec-ch-ua-mobile': '?0',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'
}

date_list = []
for yy in range(2012,2022):
    for mm in range(1,13):
        if len(str(mm)) == 1:
            mm_str = '0' + str(mm)
            date_list.append(str(yy)+str(mm_str))
        else:
            date_list.append(str(yy)+str(mm))
        
        if yy==2021 and mm==7:
            break

data = {
    'rdata_seq' : '0000000031',
    'search_sql' : 'm01',
    'search_type' : '02',
    'search_start_date' : '201201',
    'search_end_date' : '201207',
    'search_regn_cls' : '02',
    'search_tab' : 'grid',
    'search_regn_name' : ''
}

df_list = []
for dd in date_list[0:3]:
    time.sleep(uniform(1,2))

    reqq_text = requests.post(urll,headers=headers,data=data)
    tmp_df    = pd.DataFrame(json.loads(reqq_text)['dataList'])

    print(tmp_df)