# etf 가격들을 mongodb에 업로드

import pandas as pd
import os
from datetime import datetime
from pymongo import MongoClient

# MongoDB에 연결할 호스트 및 포트 정보
host = 'localhost'  # 호스트 주소
port = 27017  # 포트 번호

# MongoDB에 연결
client = MongoClient(host, port)

# 데이터베이스 선택
db = client['snowball']  # 여기서 'mydatabase'는 사용하려는 데이터베이스 이름입니다.

# 컬렉션 선택 (테이블과 유사한 개념)
collection = db['etf_price']  # 여기서 'mycollection'은 사용하려는 컬렉션 이름입니다.


# 해당 경로에 있는 모든 파일들(pdf 파일들)을 리스트로 불러오기
path_dir = 'C:/Users/LG/Desktop/졸작/ETF_closing_processed2' # pdf 파일들이 저장되어 있는 경로 입력
etf_price_list = os.listdir(path_dir)

etf_error_list = list()

# len(stock_total_list)
for i in range(len(etf_price_list)):
    if i % 100 ==0:
        print(i+1,"/",len(etf_price_list))
    try:
        etf_date = etf_price_list[i].split(".")[0]
        etf_year = int(etf_date[:4])
        etf_month = int(etf_date[4:6])
        etf_day = int(etf_date[6:])

        df_etf = pd.read_csv(path_dir+'/'+etf_price_list[i], encoding='cp949')
        df_etf.rename(columns={'종목코드': 'etf_code', '종목명': 'etf_name',
                                            '종가': 'etf_price', '시가총액':'etf_total_price'}, inplace=True)
        df_etf['etf_code'] = df_etf['etf_code'].astype(str).str.zfill(6) # 파일들에서 '종목코드' 컬럼이 어떤 파일은 object로, 어떤파일은 int로 되어 있어서 다 문자열로 교체
        df_etf['etf_date'] = etf_date
        df_etf['etf_year'] = etf_year
        df_etf['etf_month'] = etf_month
        df_etf['etf_day'] = etf_day

        upload_documents = df_etf.to_dict("records")

        result = collection.insert_many(upload_documents)
    

    except:
        # print('!!!!!!!!!!!!!!!!!!!!!!!error!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        etf_error_list.append(etf_price_list[i])
        
# 연결 종료
client.close()

    