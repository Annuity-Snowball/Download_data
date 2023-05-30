# pdf_files를 mongodb에 업로드
# 한 20분 정도 걸림
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
collection = db['pdf_files']  # 여기서 'mycollection'은 사용하려는 컬렉션 이름입니다.


# 해당 경로에 있는 모든 파일들(pdf 파일들)을 리스트로 불러오기
path_dir = 'C:/Users/LG/Desktop/졸작/pdf_files' # pdf 파일들이 저장되어 있는 경로 입력
pdf_file_list = os.listdir(path_dir)

pdf_error_list = list()


for i in range(len(pdf_file_list)):
    if i%1000 ==0:
        print(i+1,"/",len(pdf_file_list))
        print(pdf_file_list[i])
    upload_document_final = dict()
    pdf_date = pdf_file_list[i].split(".")[0].split("_")[1]
    upload_document_final['pdf_date'] = pdf_date
    upload_document_final['pdf_year'] = int(pdf_date[:4])
    upload_document_final['pdf_month'] = int(pdf_date[4:6])
    upload_document_final['pdf_day'] = int(pdf_date[6:])
    upload_document_final['etf_code'] = pdf_file_list[i].split(".")[0].split("_")[0].zfill(6)
    df_pdf =pd.read_csv(path_dir+'/'+pdf_file_list[i], encoding='cp949')
    
    upload_document_list = list()
    for j in range(len(df_pdf)):
        upload_document = dict()
        upload_document['stock_code'] = df_pdf.loc[j]['종목코드']
        upload_document['stock_name'] = df_pdf.loc[j]['구성종목명']
        upload_document['stock_count'] = float(df_pdf.loc[j]['주식수(계약수)'])
        upload_document['stock_predict_price'] = float(df_pdf.loc[j]['평가금액'])
        upload_document['stock_total_price'] = float(df_pdf.loc[j]['시가총액'])
        upload_document_list.append(upload_document)

    upload_document_final['stock_list'] = upload_document_list
    inserted_doc = collection.insert_one(upload_document_final)

# 연결 종료
client.close()
    
