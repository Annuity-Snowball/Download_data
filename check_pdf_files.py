# 셀레니움으로 크롤링한 pdf 파일들이 다 다운이 되었는지 확인

import pandas as pd
import getDatainfo
from datetime import datetime
import os

# 다운받은 파일들을 확인
file_list = os.listdir('C:\\Users\\LG\\Desktop\\pdf_files')
for i,file_name in enumerate(file_list):
    file_list[i] = file_name.split('.')[0]
print('다운받은 파일 개수 :', len(file_list))

    

# 다운 받았어야 하는 파일들 확인
df = pd.read_csv("C:\self_project\snowball\Download_data\\ad.csv")
code_list = list(df['code'])
date_list = list(df['date'])

payinDate_dict_bm = dict()

# 매달 초 나오는 것
for i in range(len(code_list)):
    payinDate_dict_bm[code_list[i]] = getDatainfo.getPayInDateInfo(date_list[i], datetime.today().strftime('%Y-%m-%d'), '0')

list1 = []
list2 = []
for stock_code in payinDate_dict_bm.keys():
    for search_date in payinDate_dict_bm[stock_code]:
        list1.append(stock_code)
        search_date = ''.join(search_date.split('-'))
        list2.append(search_date)
        
print('list1 lengh :',len(list1))
print('list2 lengh :',len(list2))

correct_list = list() # 다운 받았어야 하는 파일

for i in range(len(list1)):
    correct_list.append(str(list1[i])+'_'+list2[i])

print('다운받았어야 하는 파일 개수 :', len(correct_list))

missing_file = list()
for filename in correct_list:
    if filename in file_list:
        pass
    else:
        missing_file.append(filename)
    
print('다운 못받은 파일 개수 :',len(missing_file))
print(missing_file)
