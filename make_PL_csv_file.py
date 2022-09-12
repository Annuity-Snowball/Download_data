# 포괄연결손익계산서와 연결손익계산서 txt 파일을 csv파일로 통합해서 생성하는 코드

import pandas as pd
import os
file_list = os.listdir('C:\\Users\\LG\\Desktop\\report_PL')

print(file_list)

for i in range(len(file_list)):
    if i %2 ==1:
        print('will concat :', file_list[i-1], file_list[i])
        df_1=pd.read_csv("C:\\Users\\LG\\Desktop\\report_PL\\"+file_list[i-1],delimiter="\t", encoding='cp949')
        df_2=pd.read_csv("C:\\Users\\LG\\Desktop\\report_PL\\"+file_list[i],delimiter="\t", encoding='cp949')
        df = pd.concat([df_1, df_2])
        file_name = '_'.join(file_list[i-1].split('_')[:3])
        df.to_csv('C:\\Users\\LG\\Desktop\\financial_report\\'+file_name+'.csv', index=False,encoding='cp949') 