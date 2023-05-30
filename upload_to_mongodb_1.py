# 주식시가총액 파일을 mongodb에 업로드
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
collection = db['stock_total_price']  # 여기서 'mycollection'은 사용하려는 컬렉션 이름입니다.


# 해당 경로에 있는 모든 파일들(pdf 파일들)을 리스트로 불러오기
path_dir = 'C:/Users/LG/Desktop/졸작/stock_processed2' # pdf 파일들이 저장되어 있는 경로 입력
stock_total_list = os.listdir(path_dir)

stock_error_list = list()

# len(stock_total_list)
for i in range(len(stock_total_list)):
    if i%100 ==0 :
        print(i+1,"/",len(stock_total_list))
#         print(stock_total_list[i])
        
    try:  
        stock_date = stock_total_list[i].split(".")[0]
        stock_year = int(stock_date[:4])
        stock_month = int(stock_date[4:6])
        stock_day = int(stock_date[6:])

        df_total_stock =pd.read_csv(path_dir+'/'+stock_total_list[i], encoding='cp949')

        df_total_stock.rename(columns={'종목코드': 'stock_code', '종목명': 'stock_name',
                                        '종가': 'stock_price', '시가총액':'stock_total_price'}, inplace=True)

        df_total_stock['stock_date'] = stock_date
        df_total_stock['stock_year'] = stock_year
        df_total_stock['stock_month'] = stock_month
        df_total_stock['stock_day'] = stock_day
        df_total_stock['stock_code'] = df_total_stock['stock_code'].astype(str).str.zfill(6) # 파일들에서 '종목코드' 컬럼이 어떤 파일은 object로, 어떤파일은 int로 되어 있어서 다 문자열로 교체

        # 데이터프레임을 dictionary로 변환(upload_many를 위해서)
        upload_documents=df_total_stock.to_dict("records")
        result = collection.insert_many(upload_documents)
    
    except:
        stock_error_list.append(stock_total_list[i])
    
    
# 연결 종료
client.close()

    