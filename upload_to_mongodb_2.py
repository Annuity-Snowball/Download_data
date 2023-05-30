# 전종목기본정도 mongodb에 업로드 
import pandas as pd
import os
from datetime import datetime
from pymongo import MongoClient

df_etf_info =pd.read_csv("전종목기본정보.csv", encoding='cp949')
df_etf_info['추적배수'] = df_etf_info['추적배수'].replace(r'\s*\(.*\)', '', regex=True)
df_etf_info["start_date"] = df_etf_info["상장일"].str.replace('/','', regex=True)
df_etf_info["start_year"] = df_etf_info["상장일"].str.split('/',expand=True)[0].astype("int64")
df_etf_info["start_month"] = df_etf_info["상장일"].str.split('/',expand=True)[1].astype("int64")
df_etf_info["start_day"] = df_etf_info["상장일"].str.split('/',expand=True)[2].astype("int64")
df_etf_info['단축코드'] = df_etf_info['단축코드'].astype(str).str.zfill(6)

# MongoDB에 연결할 호스트 및 포트 정보
host = 'localhost'  # 호스트 주소
port = 27017  # 포트 번호

# MongoDB에 연결
client = MongoClient(host, port)

# 데이터베이스 선택
db = client['snowball']  # 여기서 'mydatabase'는 사용하려는 데이터베이스 이름입니다.

# 컬렉션 선택 (테이블과 유사한 개념)
collection = db['etf_information']  # 여기서 'mycollection'은 사용하려는 컬렉션 이름입니다.

for i in range(len(df_etf_info)):
    upload_document= dict()
    upload_document['etf_code'] = df_etf_info.loc[i]['단축코드']
    upload_document["start_date"] = df_etf_info.loc[i]["start_date"]
    upload_document["start_year"] = int(df_etf_info.loc[i]["start_year"])
    upload_document["start_month"] = int(df_etf_info.loc[i]["start_month"])
    upload_document["start_day"] = int(df_etf_info.loc[i]["start_day"])
    upload_document['etf_kr_full_name'] = df_etf_info.loc[i]['한글종목명']
    upload_document['etf_kr_name'] = df_etf_info.loc[i]['한글종목약명']
    upload_document['etf_en_name'] = df_etf_info.loc[i]['영문종목명']
    upload_document['base_index'] = df_etf_info.loc[i]['기초지수명']
    upload_document['follow_multiple_category'] = df_etf_info.loc[i]['추적배수']
    upload_document['base_market_category'] = df_etf_info.loc[i]['기초시장분류']
    upload_document['base_asset_catogory'] = df_etf_info.loc[i]['기초자산분류']
    upload_document['etf_company'] = df_etf_info.loc[i]['운용사']
    upload_document['etf_cu'] = int(df_etf_info.loc[i]['CU수량'])
    inserted_doc = collection.insert_one(upload_document)
    
    
# 연결 종료
client.close()

