# 금융상품 평가지표 만드는 코드
import os
import pandas as pd
from IPython.display import display
import numpy as np


def make_date_type(df):
    df['product_ticker'] = str(int(df['product_ticker']))
    return df
    
file_list = os.listdir('C:\\self_project\\snowball\\Download_data\\product_price')

df_financial=pd.read_csv("C:\\self_project\\snowball\\Download_data\\product_financial.csv",encoding='cp949')

df_product_start=pd.read_csv("C:\\self_project\\snowball\\Download_data\\after_product_start.csv",encoding='cp949')
df_product_start = df_product_start.rename(columns={"단축코드":"금융상품코드"})
del df_product_start['시작날짜']
# 재무지표들이 전무 0인 경우 제거
df_financial = df_financial.drop(df_financial[(df_financial['추정매출액'] ==0) & (df_financial['추정영업이익'] ==0)& (df_financial['추정당기순이익'] ==0)& (df_financial['추정유동자산'] ==0)& (df_financial['추정유동자산'] ==0)& (df_financial['추정자산총계'] ==0)& (df_financial['추정유동부채'] ==0)& (df_financial['추정부채총계'] ==0)].index)



# sql에 업데이트할 데이터 프레임 생성
df_sql = pd.DataFrame({}, columns=['날짜','Open','금융상품코드','추정매출액','추정영업이익','추정당기순이익','추정유동자산','추정자산총계','추정유동부채','추정부채총계'])


# 추후에 모든 가격 파일들에 대해서 반복!
for file_name in file_list:
    # print(file_name)
    df_price=pd.read_csv("C:\\self_project\\snowball\\Download_data\\product_price\\"+file_name,encoding='cp949')
    df_financial_temp = df_financial[df_financial['금융상품코드']==int(file_name.split('.')[0].split('_')[0])].copy() # df_financail 에서 해당 금융상품인 경우 추출
    df_price = df_price[['Date','Open']] # 필요한 컬럼만 사용
    df_price.Date = df_price.Date.str.split('-').str[0] + df_price.Date.str.split('-').str[1] + df_price.Date.str.split('-').str[2] # 문자열 타입이어서 '-'을 제거한후
    df_price = df_price.astype({'Date': 'int64'}) # 컬럼을 정수형으로 변환
    df_price = df_price.drop(df_price[(df_price['Date']<20170101) | (df_price['Date']>20181231) ].index)
    df_price = df_price.rename(columns={"Date":"날짜"}) # join하기 위해서 컬럼명 수정

    df_temp = pd.merge(df_price, df_financial_temp, on="날짜", how='left').copy()

    # 금융상품에 해당하는 재무정보들이 존재할 경우
    if len(df_financial_temp)>0:
        df_temp.fillna(method='ffill', inplace=True) # nan 값들을 컬럼에서 그 이전의 값으로 채움
        df_sql = pd.concat([df_sql, df_temp])

df_sql =df_sql.dropna() # 결측치들을 제거
df_sql = df_sql.rename(columns={"Open":"거래가격"})
df_sql = pd.merge(df_sql,df_product_start,on="금융상품코드", how='left')
df_sql['시가총액'] = df_sql['거래가격']*df_sql['상장좌수']
del df_sql['거래가격']
del df_sql['상장좌수']
df_sql['per']=df_sql['시가총액']/df_sql['추정당기순이익']
df_sql['pbr']=df_sql['시가총액']/df_sql['추정자산총계']
df_sql['psr']=df_sql['시가총액']/df_sql['추정매출액']
df_sql['roe']=df_sql['추정당기순이익']/(df_sql['추정자산총계']-df_sql['추정부채총계'])
df_sql['roa']=df_sql['추정당기순이익']/df_sql['추정자산총계']
df_sql['operating_to_revenue_ratio']=df_sql['추정영업이익']/df_sql['추정매출액']
df_sql['liabilities_to_assets_ratio']=df_sql['추정부채총계']/df_sql['추정자산총계']
df_sql['current_liabilities_to_assets_ratio']=df_sql['추정유동부채']/df_sql['추정유동자산']
df_sql = df_sql[['금융상품코드','날짜','per','pbr','psr','roe','roa','operating_to_revenue_ratio','liabilities_to_assets_ratio','current_liabilities_to_assets_ratio']]
df_sql = df_sql.rename(columns={'금융상품코드':"product_ticker",'날짜':'product_date'})

df_sql['product_date'] = pd.to_datetime(df_sql['product_date'], format='%Y%m%d')

df_sql = df_sql.apply(make_date_type, axis=1)

df_sql.to_csv('C:\self_project\snowball\Download_data\\product_evaluate.csv', index=False,encoding='cp949') 