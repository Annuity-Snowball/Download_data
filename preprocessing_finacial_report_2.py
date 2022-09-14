import pandas as pd
from IPython.display import display
import csv

pdf_stock_list = list() # pdf에서 사용되는 종목코드들이 담겨 있는 리스트 생성
with open('C:\\self_project\\snowball\\Download_data\\need_stock_list.csv', newline='', encoding='utf-8') as csvfile:
    pre_pdf_stock_list = list(csv.reader(csvfile, delimiter=' ')) # need_stock_list.csv 파일에서 종목코드들을 불러옴


for pdf_stock_code in pre_pdf_stock_list:
    pdf_stock_list.append(pdf_stock_code[0]) # 불러온 종목코드가 각각 리스트로 되어 있으므로, 문자열로 바꾸어 주는 부분이 필요 함!



PL_info = ['2016_1Q_PL.txt','당기 1분기 누적','2016_1Q_PL.csv']

df_text=pd.read_csv("C:\\Users\\LG\\Desktop\\financial_report\\"+PL_info[0],delimiter="\t", encoding='cp949')

def stock_code_preprocessing(df_data):
    stock_code = df_data['종목코드']
    stock_code = stock_code[1:-1]
    df_data['종목코드'] = stock_code
    return df_data

    
# 가져온 데이터프레임에서 필요한 컬럼명만 추출
df_base = df_text.copy() # 불러온 df에 영향을 주지 않기 위해서 copy 사용
df_base = df_base.apply(stock_code_preprocessing,axis=1) # 종목코드의 [] 을 제거하는 함수 적용, df를 건들지 말고 df_base를 참조


df_base = df_base.drop(df_base[~df_base['종목코드'].isin(pdf_stock_list)].index) 


df_PL = pd.read_csv("C:\\Users\\LG\\Desktop\\financial_report\\2016_1Q_PL.csv", encoding='cp949')