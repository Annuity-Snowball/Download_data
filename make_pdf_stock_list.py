# 재무제표에 누락된 수치들이 많아서 필요한 종목들만 추려야 할듯 따라서 
# ETF PDF 에 있는 종목 코드들만 따오기
# need_stock_list.csv 은 etf pdf 파일들에 있는 종목코드들

import pandas as pd
import os
import csv

path_dir = 'C:/Users/LG/Desktop/pdf_files' # pdf 파일들이 저장되어 있는 경로 입력
file_list = os.listdir(path_dir) # pdf파일 경로에 있는 모든 pdf 파일들 명을 file_list로 저장

pdf_stock_list = list() # 재무제표에서 조회해야 할 종목코드 들
file_list_len = len(file_list) # 진행과정을 확인하기 위해서 file_list 의 크기를 구함


for i,file_name in enumerate(file_list): # file_list 들에 대해서 반복
    print(file_name, f'({i}/{file_list_len})') # 진행 정도를 print
    df = pd.read_csv(path_dir+'/'+file_name, encoding='cp949') # 파일을 ㅇ릭음
    pdf_stock_list += list(df['종목코드']) # pdf 파일의 column이 '종목코드'인 column을 list 화 한뒤 ,npdf_stock_list에 더함
    pdf_stock_list = list(set(pdf_stock_list)) #  # set()을 통해서 겹치는 종목코드를 제거하고 다시 리스트화
    
print()
print(len(pdf_stock_list)) # 만들어진 pdf_stock_listt의 크기 출력
print(pdf_stock_list)# 만들어진 pdf_stock_list출력


with open("C:\self_project\snowball\Download_data\\pdf_stock_list.csv",'w', newline ='') as f:
    # using csv.writer method from CSV package
    write = csv.writer(f)
    for pdf_stock in pdf_stock_list:
        row=list() # 하나의 행에 저장을 할 list 초기화
        row.append(pdf_stock) # 리스트로 저장을 해야함 이렇게 안하면 문자열이 문자 하나하나 나누어 져서 저장이 됨
        write.writerow(row) # 한 행에 값을 적음
