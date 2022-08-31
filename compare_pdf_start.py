# pdf 파일의 시작날짜와, 거래가격의 시작날짜 비교하는 코드
import os
import pandas as pd

pdf_dict=dict()
price_dict = dict()
pdf_file_list = os.listdir('C:\\Users\\LG\\Desktop\\pdf_files') # pdf 파일들 경로
price_file_list = os.listdir('C:\self_project\snowball\Download_data\product_price') # 금융상품 가격들 파일 경로

for i,pdf_file_name in enumerate(pdf_file_list):
    pdf_file_list[i] = pdf_file_name.split('.')[0]
    if pdf_file_list[i].split('_')[0] not in pdf_dict:
        pdf_dict[pdf_file_list[i].split('_')[0]] = int(pdf_file_list[i].split('_')[1])

print('pdf_dict :',pdf_dict)
print('len(pdf_dict) :',len(pdf_dict))

for i,price_file_name in enumerate(price_file_list):
    df = pd.read_csv('C:\self_project\snowball\Download_data\product_price\\'+price_file_name)
    start_date = df['Date'][0]
    start_date = ''.join(start_date.split('-'))
    # print(price_file_name, df['Date'][0])
    price_file_list[i] = str(int(price_file_name.split('_')[0]))
    price_dict[price_file_list[i]] = int(start_date)
 
print()   
# print('price_file_list :', price_file_list)
print('price_dict :',price_dict)
print('len(price_dict) :',len(price_dict))

pdf_early= list()
price_early = list()
pdf_price_same = list()

for product_code in pdf_dict.keys():
    if pdf_dict[product_code] < price_dict[product_code]: # pdf의 날짜가 더 작을 때 즉, pdf가 먼저일때
        pdf_early.append(product_code)
    elif pdf_dict[product_code] > price_dict[product_code]: # pdf의 날짜가 더 zmf 때 즉, pdf가 나중일때
        price_early.append(product_code)
    else:
        pdf_price_same.append(product_code)

print()
print("pdf가 먼저 :",pdf_early) # 이런 경우는 없는 걸로 나옴!
print("금융상품 거래가격이 먼저 :",price_early)
print("두개날짜가 같음 :",pdf_price_same)