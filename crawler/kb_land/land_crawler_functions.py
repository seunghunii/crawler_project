import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import re
import requests
from time import sleep
import json

def data_from_graph1(datum):
    tmp_list = []
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

        tmp_list.append(return_df_without_data)

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
        tmp_list.append(return_df_with_data)

    return tmp_list