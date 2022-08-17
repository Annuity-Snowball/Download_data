import pandas as pd

df = pd.read_csv("C:\self_project\snowball\Download_data\\ad.csv")
code_list = list(df['code'])
date_list = list(df['date'])

product_dict = dict()
for i in range(len(code_list)):
    product_dict[code_list[i]] = date_list[i]


print(product_dict)