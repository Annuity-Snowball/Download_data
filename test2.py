import pandas as pd

df = pd.read_csv("C:\self_project\snowball\Download_data\\ad.csv")
code_list = list(df['code'])
date_list = list(df['date'])

product_dict = dict()
for i in range(len(code_list)):
    product_dict[code_list[i]] = date_list[i]


<<<<<<< HEAD
list1 = []
list2 = []
for stock_code in payinDate_dict_bm.keys():
    for search_date in payinDate_dict_bm[stock_code]:
        list1.append(stock_code)
        list2.append(search_date)
=======
print(product_dict)
>>>>>>> 7a26a8509a6cdfe02d69383bbaa64b096b14d733
