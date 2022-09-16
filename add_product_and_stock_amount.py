# 금융상품(product_start.csv)과 주식(pdf_kr_stock_list) 2개에 상장좌수들을 업데이트하는 함수
# compare_pdf_start.py 와 make_pdf_kr_stock_list.py 가 우선적으로 실행 된 다음에 실행을 해야 한다.

import pandas as pd
import csv
import numpy as np




# 주식의 상장 좌수들을 업데이트 하는 함수
def add_stock_amount():

    # 상장된 모든 주식들의 좌수를 데이터프레임으로 불러옴
    df_stock_amount = pd.read_csv('C:\\self_project\\snowball\\Download_data\\stock_baseinfo.csv', encoding='cp949')
    df_stock_amount = df_stock_amount[['단축코드','상장주식수']]

    # pdf_kr_stock_list 를 불러옴
    pdf_stock_list = list()
    with open('C:\\self_project\\snowball\\Download_data\\pdf_kr_stock_list.csv', newline='', encoding='utf-8') as csvfile:
        pre_pdf_kr_stock_list = list(csv.reader(csvfile, delimiter=' ')) # need_stock_list.csv 파일에서 종목코드들을 불러옴

    for pdf_stock_code in pre_pdf_kr_stock_list:
        pdf_stock_list.append(pdf_stock_code[0]) # 불러온 종목코드가 각각 리스트로 되어 있으므로, 문자열로 바꾸어 주는 부분이 필요 함!
        
    # pdf 내에 있는 주식들의 상장좌수들을 저장할 빈 데이터프레임 생성
    df_pdf_stock = pd.DataFrame()
    df_pdf_stock['단축코드'] = pdf_stock_list

    # df_pdf_stock 와 df_stock_amoun left join을 통해서 상장주식수가 있는 pdf_stock dataframe 생성
    df_final = pd.merge(df_pdf_stock,df_stock_amount,on='단축코드',how='left')
    df_final = df_final.fillna(0) # 결측치를 0으로 처리, 채권들도 pdf_stock 에 있따..ㅠ
    df_final.to_csv('C:\\self_project\\snowball\\Download_data\\after_pdf_kr_stock_list.csv', index=False,encoding='cp949') # 파일로 저장
    
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
# add_stock_amount()
# add_product_amount()
