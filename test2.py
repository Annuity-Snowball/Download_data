import pandas as pd
import getDatainfo
from datetime import datetime

df = pd.read_csv("C:\self_project\snowball\Download_data\\ad.csv")
code_list = list(df['code'])
date_list = list(df['date'])

# dailyDate_dict = dict()
payinDate_dict_bm = dict()
# payinDate_dict_lm = dict()

#for i in range(len(code_list)):
    #product_dict[code_list[i]] = date_list[i]


# 매일 나오는 것
# for i in range(len(code_list)):
#     dailyDate_dict[code_list[i]] = getDailyDateInfo(date_list[i], datetime.today().strftime('%Y-%m-%d'))
# print(dailyDate_dict)

# 매달 초 나오는 것
for i in range(len(code_list)):
    payinDate_dict_bm[code_list[i]] = getDatainfo.getPayInDateInfo(date_list[i], datetime.today().strftime('%Y-%m-%d'), '0')

# print(payinDate_dict_bm)

# 매달 말 나오는것
# for i in range(len(code_list)):
#     payinDate_dict_bm[code_list[i]] = getDatainfo.getPayInDateInfo(date_list[i], datetime.today().strftime('%Y-%m-%d'), 'last')

# print(payinDate_dict_lm)
list1 = []
list2 = []
for stock_code in payinDate_dict_bm.keys():
    for search_date in payinDate_dict_bm[stock_code]:
        list1.append(stock_code)
        list2.append(search_date)
print(len(list1))
print()
print(len(list2))
print(list1[:10])
print()
print(list2[:10])
