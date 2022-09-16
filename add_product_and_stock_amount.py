# 금융상품(product_start.csv)과 주식(pdf_kr_stock_list) 2개에 상장좌수들을 업데이트하는 함수
# compare_pdf_start.py 와 make_pdf_kr_stock_list.py 가 우선적으로 실행 된 다음에 실행을 해야 한다.

import pandas as pd
import csv
import numpy as np





# 금융상품의 상장 좌수들을 업데이트 함수
def add_product_amount():    
    # 상장된 모든 금융상품들의 좌수를 데이터프레임으로 불러옴
    df_product_amount = pd.read_csv('C:\\self_project\\snowball\\Download_data\\product_baseinfo.csv', encoding='cp949')
    df_product_amount = df_product_amount[['단축코드','상장좌수']]

    # product_start.csv 를 불러옴
    df_product_start = pd.read_csv('C:\\self_project\\snowball\\Download_data\\product_start.csv', encoding='cp949')
    df_product_start.columns = ['단축코드', '시작날짜']

    # 상장주식수가 있는 데이터프레임 생성위해서 left join을 활용
    df_final = pd.merge(df_product_start,df_product_amount,on='단축코드',how='left')
    df_final.to_csv('C:\\self_project\\snowball\\Download_data\\after_product_start.csv', index=False,encoding='cp949') # 파일로 저장
    
# 함수 실행
# add_product_amount()
