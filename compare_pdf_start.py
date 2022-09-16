# pdf 파일의 시작날짜와, 거래가격의 시작날짜 비교하는 코드
# 금융상품의 시작날짜인 product_start.csv를 만들기도 함!
# 결과적으로는 상품의 거래가격 시작이 pdf알 수 잇는 날짜보다 먼저 이므로, pdf 알수 있는 날짜를 시작 날짜로 계산해 버리자!
import os
import pandas as pd

pdf_dict=dict() # '금융상품명' : 'pdf시작날짜' 가 담길 dict
price_dict = dict() # '금융상품명' : '거래시작일자 가 담길 dict
pdf_file_list = os.listdir('C:\\Users\\LG\\Desktop\\pdf_files') # pdf 파일들 경로
price_file_list = os.listdir('C:\self_project\snowball\Download_data\product_price') # 금융상품 가격들 파일 경로

df_product = pd.DataFrame({},columns=['start_date']) # 금융상품의 시작날짜를 만들 데이터프레임
df_product.index.name = 'product_code' # 데이터프레임의 인덱스명을 설정
for i,pdf_file_name in enumerate(pdf_file_list): # 저장되어있는 pdf파일들에 대해서 반복
    pdf_file_list[i] = pdf_file_name.split('.')[0] # .csv 부분 제거
    if pdf_file_list[i].split('_')[0] not in pdf_dict: # 저장되어있는 pdf파일이 생성할 pdf_dict에 저장이 안되어 있다면(저장되어있는 pdf파일들은 금융상품코드가 겹치는 경우가 많으므로 이렇게 구현)
        pdf_dict[pdf_file_list[i].split('_')[0]] = int(pdf_file_list[i].split('_')[1]) # pdf_dict에 업데이트
        df_product.loc[pdf_file_list[i].split('_')[0]] = [pdf_dict[pdf_file_list[i].split('_')[0]]] # df_product 데이터프레임에 업데이트

# print('pdf_dict :',pdf_dict)
# print('len(pdf_dict) :',len(pdf_dict))
df_product=df_product.reset_index('product_code') # 인덱스를 컬럼으로 수정
print(df_product.head()) # 데이터프레임 확인위해서 head 이용
# 파일로 저장!!!!!!!!!!!
# df_product.to_csv('C:\self_project\snowball\Download_data\product_start.csv',index=False) # csv 파일로 저장

for i,price_file_name in enumerate(price_file_list):
    df = pd.read_csv('C:\self_project\snowball\Download_data\product_price\\'+price_file_name) # 해당파일을 읽음
    start_date = df['Date'][0] # 가장 첫번째 줄의 값(거래시작 날짜를 ) 가져옴
    start_date = ''.join(start_date.split('-')) # 정규표현식으로 수정
    # print(price_file_name, df['Date'][0])
    price_file_list[i] = str(int(price_file_name.split('_')[0])) # price_file_list 갱신
    price_dict[price_file_list[i]] = int(start_date) # price_dict 추가
 
# print()   
# print('price_file_list :', price_file_list)
# print('price_dict :',price_dict)
# print('len(price_dict) :',len(price_dict))

pdf_early= list()
price_early = list()
pdf_price_same = list()

# pdf파일과, 거래가격 파일 비교
for product_code in pdf_dict.keys():
    if pdf_dict[product_code] < price_dict[product_code]: # pdf의 날짜가 더 작을 때 즉, pdf가 먼저일때
        pdf_early.append(product_code)
    elif pdf_dict[product_code] > price_dict[product_code]: # pdf의 날짜가 더 zmf 때 즉, pdf가 나중일때
        price_early.append(product_code)
    else:
        pdf_price_same.append(product_code)

# print()
print("pdf가 먼저 :",pdf_early) # 이런 경우는 없는 걸로 나옴!
print("금융상품 거래가격이 먼저 :",price_early)
print("두개날짜가 같음 :",pdf_price_same)

