import FinanceDataReader as fdr
import pandas as pd

# 금융상품(etf)들의 정보가 담겨있는 파일 불러오기 
df = pd.read_csv("C:\self_project\snowball\Download_data\\ad.csv")
code_list = list(df['code']) # 컬럼며이 'code'은 필드 가져옴
for i,product_code in enumerate(code_list):
    product_code = str(product_code)
    if len(product_code)<6:
        code_list[i] ='0'+product_code
# 모든 종목코드들에 대해서 반복
for product_code in code_list:
    product_code = str(product_code)
    # 한국거래소 상장종목 전체
    df = fdr.DataReader(product_code, '2000') # dataReader 라이브러리 통해서 가격 정보 가져옴
    df = df.reset_index('Date')
    df.to_csv('C:\self_project\snowball\Download_data\product_price\\'+product_code+'_price.csv',index=False)
    print(df.head())
    print(product_code+' is completed!')
    print()