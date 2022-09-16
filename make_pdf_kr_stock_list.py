# pdf 를 이루는 종목코드들이 해외종목들도 있어서 국내 종목들만 추리는 함수

import pandas as pd
from IPython.display import display
import csv

pdf_stock_list = list() # pdf에서 사용되는 종목코드들이 담겨 있는 리스트 생성
with open('C:\\self_project\\snowball\\Download_data\\need_stock_list.csv', newline='', encoding='utf-8') as csvfile:
    pre_pdf_stock_list = list(csv.reader(csvfile, delimiter=' ')) # need_stock_list.csv 파일에서 종목코드들을 불러옴


for pdf_stock_code in pre_pdf_stock_list:
    pdf_stock_list.append(pdf_stock_code[0]) # 불러온 종목코드가 각각 리스트로 되어 있으므로, 문자열로 바꾸어 주는 부분이 필요 함!

kr_stock_list = list()

for pdf_stock_code in pdf_stock_list:
    if len(pdf_stock_code)==6:
        kr_stock_list.append(pdf_stock_code)


print(kr_stock_list)
print(len((kr_stock_list)))


with open("C:\self_project\snowball\Download_data\\pdf_kr_stock_list.csv",'w', newline ='') as f:
    # using csv.writer method from CSV package
    write = csv.writer(f)
    for kr_stock in kr_stock_list:
        row=list() # 하나의 행에 저장을 할 list 초기화
        row.append(kr_stock) # 리스트로 저장을 해야함 이렇게 안하면 문자열이 문자 하나하나 나누어 져서 저장이 됨
        write.writerow(row) # 한 행에 값을 적음