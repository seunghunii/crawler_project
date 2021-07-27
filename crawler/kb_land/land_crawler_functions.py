import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import re
import requests
from time import sleep
import json

def data_from_graph1(datum):
    tmp_list1 = []
    search_graph1 = re.search('var graphYn1 = [$](.+?);', datum[1]['req_text'], re.S)

    if search_graph1 is None:
        return_df_without_data = pd.DataFrame({
            'year': datum[1]['year'],
            'month': datum[1]['month'],
            'region_b': datum[1]['region_b'],
            'region_s': datum[1]['region_s'],
            'ref_date': 0,
            'jisu_v': 0,
            'jisu_d': 0
        }, index=[0])

        tmp_list1.append(return_df_without_data)

    else:

        jisu_split = search_graph1.group(1)
        jisu_split = jisu_split.replace(".trim('[", "").replace("') == '' ? false: true", "").replace('Date.UTC(', '')
        jisu_split = jisu_split.split('], [')

        date_list_jisu = []
        data_list_jisu = []

        for jisu in jisu_split:
            jisu_parser = jisu.split('), ')

            jisu_date_parser = jisu_parser[0].replace(' ', '').split(',')

            date_list_jisu.append(','.join([
                jisu_date_parser[0],
                str(int(jisu_date_parser[1]) + 1),
                jisu_date_parser[2]]))

            data_list_jisu.append(jisu_parser[1].replace(']', '').replace(',', ''))

        ref_date = re.search('<p class="date">(.+?)</p>', datum[1]['req_text'])[0]
        ref_date = re.sub('<.*?>', '', ref_date, re.S)

        return_df_with_data = pd.DataFrame({
            'year': datum[1]['year'],
            'month': datum[1]['month'],
            'region_b': datum[1]['region_b'],
            'region_s': datum[1]['region_s'],
            'ref_date': ref_date,
            'jisu_v': data_list_jisu,
            'jisu_d': date_list_jisu
        })
        tmp_list1.append(return_df_with_data)

    return tmp_list1

def data_from_graph2(datum):
    tmp_list2 = []
    search_graph2_a = re.search('var graphYn2 = [$](.+?);',datum[1]['req_text'],re.S)
    search_graph2_b = re.search("var graphYn2 = [$].trim\(.{1,2}\)", datum[1]['req_text'], re.S)
    
    if (search_graph2_a is None) or (search_graph2_b is not None):
        return_df_without_data = pd.DataFrame({
            'year'     : datum[1]['year'],
            'month'    : datum[1]['month'],
            'region_b' : datum[1]['region_b'],
            'region_s' : datum[1]['region_s'],
            'ref_date' : 0,
            'rate_v'   : 0,
            'rate_d'   : 0
        },index=[0])
        
        tmp_list2.append(return_df_without_data)
    
    else:
    
        rate_split = re.search('var graphYn2 = [$](.+?);', datum[1]['req_text'], re.S).group(1)
        rate_split = rate_split.replace(".trim('[", "").replace("') == '' ? false: true", "").replace('Date.UTC(', '')
        rate_split = rate_split.split('], [')
        
        date_list_rate = []
        data_list_rate = []
        
        for rate in rate_split:
            rate_parser = rate.split('), ')

            rate_date_parser = rate_parser[0].replace(' ','').split(',')

            date_list_rate.append(','.join([
                rate_date_parser[0],
                str(int(rate_date_parser[1]) + 1),
                rate_date_parser[2]]))
            
            data_list_rate.append(rate_parser[1].replace(']','').replace(',',''))
            
        ref_date = re.search('<p class="date">(.+?)</p>',datum[1]['req_text'])[0]
        ref_date = re.sub('<.*?>','',ref_date,re.S)
        
        return_df_with_data = pd.DataFrame({
            'year'     : datum[1]['year'],
            'month'    : datum[1]['month'],
            'region_b' : datum[1]['region_b'],
            'region_s' : datum[1]['region_s'],
            'ref_date' : ref_date,
            'rate_v'   : data_list_rate,
            'rate_d'   : date_list_rate
        })
        
        tmp_list2.append(return_df_with_data)

    return tmp_list2