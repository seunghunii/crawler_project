from main.kbland.crawler.price_land_crawler_functions import data_from_graph1, data_from_graph2
import pandas as pd

dirr     = 'C:/Users/rsh15/Google Drive/crawler_data/kbland/meta/seju_kb_land_req_text.csv'
seju_dir = 'C:/Users/rsh15/Google Drive/crawler_data/kbland/seju'
dataa   = pd.read_csv(dirr)

graph1_list = []
graph2_list = []
for data_iter in dataa.iterrows():
    graph1_list.append(data_from_graph1(data_iter[1]))
    graph2_list.append(data_from_graph2(data_iter[1]))

df_jisu = pd.concat(graph1_list,axis=0)
df_jisu.to_csv(seju_dir + '/매매가격_지수_original_seju.csv',index=False)

df_rate = pd.concat(graph2_list,axis=0)
df_rate.to_csv(seju_dir + '/매매가격_변화율_original_seju.csv',index=False)