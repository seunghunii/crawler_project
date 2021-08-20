from market_land_crawler_functions import market_data_from_graph1, market_data_from_graph2
import pandas as pd

dirr    = 'C:/Users/shic/Desktop/crawler_project/data_save/kb_land/kb_land_req_text.csv'
dataa   =  pd.read_csv(dirr)

graph1_list = []
graph2_list = []
for data_iter in dataa.iterrows():
    graph1_list.append(market_data_from_graph1(data_iter[1]))
    graph2_list.append(market_data_from_graph2(data_iter[1]))

df_jisu = pd.concat(graph1_list,axis=0)
df_jisu['jisu_v'] = df_jisu['jisu_v'].astype(float)
df_jisu['jisu_d_conv'] = pd.to_datetime(df_jisu['jisu_d'],format='%Y,%m,%d')
df_jisu['jisu_d_week'] = [k.isocalendar()[1] for k in df_jisu['jisu_d_conv']]
df_jisu_preprocess = df_jisu.groupby(['year','month','region_b','region_s','jisu_d_week','date_100'],as_index=False)['jisu_v'].mean()
df_jisu_preprocess.to_csv('C:/Users/shic/Desktop/crawler_project/data_save/kb_land/processed/매매시장_매수우위_preprocessed.csv',index=False)

df_rate = pd.concat(graph2_list,axis=0)
df_rate['rate_v'] = df_rate['rate_v'].astype(float)
df_rate['rate_d_conv'] = pd.to_datetime(df_rate['rate_d'],format='%Y,%m,%d')
df_rate['rate_d_week'] = [k.isocalendar()[1] for k in df_rate['rate_d_conv']]
df_rate_preprocess = df_rate.groupby(['year','month','region_b','region_s','rate_d_week','date_100'],as_index=False)['rate_v'].mean()
df_rate_preprocess.to_csv('C:/Users/shic/Desktop/crawler_project/data_save/kb_land/processed/매매시장_매매거래_preprocessed.csv',index=False)