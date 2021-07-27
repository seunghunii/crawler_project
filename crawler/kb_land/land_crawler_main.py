from land_crawler_functions import data_from_graph1, data_from_graph2
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import re
import requests
from time import sleep
import json

dirr    = 'C:/Users/shic/Desktop/kb_land_req_text.csv'
dataa   = pd.read_csv(dirr)

graph1_list = []
graph2_list = []
for data_iter in dataa.iterrows():
    graph1_list.append(data_from_graph1(data_iter[1]))
    graph2_list.append(data_from_graph2(data_iter[1]))

df_jisu = pd.concat(graph1_list,axis=0)
df_jisu.to_csv('C:/Users/shic/Desktop/crawler_project/data_save/kb_land/final/매매가격_지수.csv')

df_rate = pd.concat(graph2_list,axis=0)
df_rate.to_csv('C:/Users/shic/Desktop/crawler_project/data_save/kb_land/final/매매가격_변화율.csv')