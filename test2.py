import pandas as pd
import getDatainfo
from datetime import datetime

df = pd.read_csv("ad.csv")
code_list = list(df['code'])
date_list = list(df['date'])

dailyDate_dict = dict()
payinDate_dict_bm = dict()
payinDate_dict_lm = dict()

#for i in range(len(code_list)):
    #product_dict[code_list[i]] = date_list[i]

#
""" for i in range(len(code_list)):
    dailyDate_dict[code_list[i]] = getDailyDateInfo(date_list[i], datetime.today().strftime('%Y-%m-%d'))
print(dailyDate_dict)
"""

for i in range(len(code_list)):
    payinDate_dict_bm[code_list[i]] = getDatainfo.getPayInDateInfo(date_list[i], datetime.today().strftime('%Y-%m-%d'), 'first')

print(payinDate_dict_bm)

for i in range(len(code_list)):
    payinDate_dict_bm[code_list[i]] = getDatainfo.getPayInDateInfo(date_list[i], datetime.today().strftime('%Y-%m-%d'), 'last')

print(payinDate_dict_lm)