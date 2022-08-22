# 셀레니움으로 크롤링한 pdf 파일들이 다 다운이 되었는지 확인

import pandas as pd
import getDatainfo
from datetime import datetime
import os

# 다운받은 파일들을 확인
file_list = os.listdir('C:/Users/LG/Desktop/PDF_files')
for i,file_name in enumerate(file_list):
    file_list[i] = file_name.split('.')[0].split('_')
print(file_list[:10])

    


# df = pd.read_csv("C:\self_project\snowball\Download_data\\ad.csv")
# code_list = list(df['code'])
# date_list = list(df['date'])

# payinDate_dict_bm = dict()

# # 매달 초 나오는 것
# for i in range(len(code_list)):
#     payinDate_dict_bm[code_list[i]] = getDatainfo.getPayInDateInfo(date_list[i], datetime.today().strftime('%Y-%m-%d'), 'first')

# list1 = []
# list2 = []
# for stock_code in payinDate_dict_bm.keys():
#     for search_date in payinDate_dict_bm[stock_code]:
#         list1.append(stock_code)
#         list2.append(search_date)
        
        
# print(list1[:10])
# print(list2[:10])
