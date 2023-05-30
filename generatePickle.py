import getDatainfo
import pandas as pd
from datetime import datetime
import csv

df = pd.read_csv("ad.csv")
code_list = list(df['code'])
date_list = list(df['date'])
payinDate_dict_bm = dict()
print('after ad.csv')

for i in range(len(code_list)):
    payinDate_dict_bm[code_list[i]] = getDatainfo.getPayInDateInfo(date_list[i],
                                                                   datetime.today().strftime('%Y-%m-%d'), '0')
print('after payinDate')
product_code_list = []
product_date_list = []
for stock_code in payinDate_dict_bm.keys():
    for search_date in payinDate_dict_bm[stock_code]:
        product_code_list.append(stock_code)
        product_date_list.append(search_date)
print('after product_code and date list')

df = pd.DataFrame(zip(product_code_list, product_date_list), columns=['code', 'date'])
df.to_pickle('code_date.pkl') # pickle 형식으로 저장

data = pd.read_pickle('code_date.pkl') # 변환 확인
print(data)
