import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import re
import requests
from time import sleep
import json

def data_from_graph1(datum):

    # 기준일자 파싱.
    ref_date_detect = re.search('<p class="date">(.+?)</p>', datum['req_text'])
        
    if ref_date_detect is None:
        ref_date = '(기준일: 1900.01.01)'
    else:
        ref_date = re.sub('<.*?>', '',ref_date_detect[0], re.S)

    # (2019.01.14=100.0) 형태로 되어 있는 지수의 기준일자 파싱
    date_100_detect = re.search('\(\d{,4}.\d{,2}.\d{,2}=100.0\)',datum['req_text'],re.S)

    if date_100_detect is None:
        date_100 = '(1900.01.01=999.0)'
    else:
        date_100 = date_100_detect[0]

    # 페이지에 상단, 하단 두 개의 그래프가 있음.
    # 상단의 그래프 데이터만을 파싱하기 위해
    # 하단 그래프의 제목 인덱스 전까지의 텍스트를 활용.
    divider = '<h3>주간 매매시장 동향<span class="sub">'
    divider_idx1 = datum['req_text'].find(divider)
    req_text_parse1 = datum['req_text'][divider_idx1:]

    # 그래프 데이터를 담고 있는 var graphYn1
    search_graph1 = re.search('var graphYn1 = [$](.+?);', req_text_parse1, re.S)

    # var graphYn1은 무조건 있지만,
    # 데이터가 조회되지 않는 경우에는 0이 들어간 데이터를 return
    if search_graph1 is None:
        return_df_without_data = pd.DataFrame({
            'year': datum['year'],
            'month': datum['month'],
            'region_b': datum['region_b'],
            'region_s': datum['region_s'],
            'ref_date': ref_date,
            'date_100' : date_100,
            'jisu_v': 9999,
            'jisu_d': '1900,1,1'
        }, index=[0])

        return return_df_without_data

    # var graphYn1 태그가 데이터를 가지고 있는 경우
    else:

        # 데이터 파싱.
        # 텍스트에서 필요없는 앞뒤 태그나 코드 제거.
        jisu_split = search_graph1.group(1)
        jisu_split = jisu_split.replace(".trim('[", "").replace("') == '' ? false: true", "").replace('Date.UTC(', '')
        jisu_split = jisu_split.split('], [')

        date_list_jisu = []
        data_list_jisu = []

        # var graphYn1이 가지고 있는 데이터만을 남긴 뒤,
        # loop를 돌려 각 행별로 파싱.
        for jisu in jisu_split:
            jisu_parser = jisu.split('), ')

            jisu_date_parser = jisu_parser[0].replace(' ', '').split(',')

            # date에 월이 -1된 값으로 저장되어 있어 1을 더함.
            date_list_jisu.append(','.join([
                jisu_date_parser[0],
                str(int(jisu_date_parser[1]) + 1),
                jisu_date_parser[2]]))

            data_list_jisu.append(jisu_parser[1].replace(']', '').replace(',', ''))

        # 파싱된 데이터와 인덱스를 조합하여 DataFrame을 만들고, return함.
        return_df_with_data = pd.DataFrame({
            'year': datum['year'],
            'month': datum['month'],
            'region_b': datum['region_b'],
            'region_s': datum['region_s'],
            'ref_date': ref_date,
            'date_100' : date_100,
            'jisu_v': data_list_jisu,
            'jisu_d': date_list_jisu
        })

        return return_df_with_data

def data_from_graph2(datum):

    # 기준일자 파싱.
    ref_date_detect = re.search('<p class="date">(.+?)</p>', datum['req_text'])
        
    if ref_date_detect is None:
        ref_date = '(기준일: 1900.01.01)'
    else:
        ref_date = re.sub('<.*?>', '',ref_date_detect[0], re.S)

    # (2019.01.14=100.0) 형태로 되어 있는 지수의 기준일자 파싱
    date_100_detect = re.search('\(\d{,4}.\d{,2}.\d{,2}=100.0\)',datum['req_text'],re.S)

    if date_100_detect is None:
        date_100 = '(1900.01.01=999.0)'
    else:
        date_100 = date_100_detect[0]
    
    # 페이지에 상단, 하단 두 개의 그래프가 있음.
    # 상단의 그래프 데이터만을 파싱하기 위해
    # 하단 그래프의 제목 인덱스 전까지의 텍스트를 활용.
    divider = '<h3>주간 매매시장 동향<span class="sub">'
    divider_idx2 = datum['req_text'].find(divider)
    req_text_parse2 = datum['req_text'][divider_idx2:]
    
    # 그래프 데이터를 담고 있는 var graphYn2
    search_graph2_a = re.search('var graphYn2 = [$](.+?);',req_text_parse2,re.S)
    search_graph2_b = re.search("var graphYn2 = [$].trim\(.{1,2}\)",req_text_parse2, re.S)
    
    # var graphYn2은 무조건 있지만,
    # 데이터가 조회되지 않는 경우나
    # 데이터에 변화가 없어 지수만 있고 변화율은 존재하지 않는 경우 0이 들어간 데이터를 return
    if (search_graph2_a is None) or (search_graph2_b is not None):
        return_df_without_data = pd.DataFrame({
            'year'     : datum['year'],
            'month'    : datum['month'],
            'region_b' : datum['region_b'],
            'region_s' : datum['region_s'],
            'ref_date' : ref_date,
            'date_100' : date_100,
            'rate_v'   : 9999,
            'rate_d'   : '1900,1,1'
        },index=[0])
        
        return return_df_without_data
    
    # var graphYn2 태그가 데이터를 가지고 있는 경우
    else:
    
        # 데이터 파싱.
        # 텍스트에서 필요없는 앞뒤 태그나 코드 제거.
        rate_split = re.search('var graphYn2 = [$](.+?);', req_text_parse2, re.S).group(1)
        rate_split = rate_split.replace(".trim('[", "").replace("') == '' ? false: true", "").replace('Date.UTC(', '')
        rate_split = rate_split.split('], [')
        
        date_list_rate = []
        data_list_rate = []
        
        # var graphYn2이 가지고 있는 데이터만을 남긴 뒤,
        # loop를 돌려 각 행별로 파싱.
        for rate in rate_split:
            rate_parser = rate.split('), ')

            rate_date_parser = rate_parser[0].replace(' ','').split(',')

            # date에 월이 -1된 값으로 저장되어 있어 1을 더함.
            date_list_rate.append(','.join([
                rate_date_parser[0],
                str(int(rate_date_parser[1]) + 1),
                rate_date_parser[2]]))
            
            data_list_rate.append(rate_parser[1].replace(']','').replace(',',''))
            
        # 파싱한 데이터와 인덱스를 조합하여 DataFrame을 만들고, return함.
        return_df_with_data = pd.DataFrame({
            'year'     : datum['year'],
            'month'    : datum['month'],
            'region_b' : datum['region_b'],
            'region_s' : datum['region_s'],
            'ref_date' : ref_date,
            'date_100' : date_100,
            'rate_v'   : data_list_rate,
            'rate_d'   : date_list_rate
        })
        
        return return_df_with_data
