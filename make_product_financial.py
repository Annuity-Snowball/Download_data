# pdf 재무지표들 생성하는 코드! -1차, 2차에서는 일자 범위내에 모든 가격들을 통해서 '평가지표'들 생성!!!
import os
import pandas as pd
from IPython.display import display
import numpy as np

# 결산기준일이 날짜형태로 되어 있는데 가장 가까운 날로 구하기 위해서 정수화
def make_date_to_int(df):
    df['결산기준일'] = int(''.join(df['결산기준일'].split('-')))
    return df
    
# 종목코드에 0을 붙이는 코드
def add_0_to_stock_code(df):
    df['종목코드'] = (6-len(str(int(df['종목코드']))))*'0'+str(int(df['종목코드']))
    return df

# 손익계산서를 업데이트 하는 함수
def update_dfPL_to_dfpdf(df_pdf):
    # 재무제표에서 해당주식 정보가 준비할 경우 업데이트
    if len(df_need_PL[df_need_PL['종목코드'] == df_pdf['종목코드']])>0:
        df_pdf['매출액'] = df_need_PL[df_need_PL['종목코드'] ==df_pdf['종목코드']].iloc[-1]['매출액'] # float()로 묶는 것도 안되면 고려해보자
        df_pdf['영업이익'] = df_need_PL[df_need_PL['종목코드'] == df_pdf['종목코드']].iloc[-1]['영업이익']
        df_pdf['당기순이익'] = df_need_PL[df_need_PL['종목코드'] == df_pdf['종목코드']].iloc[-1]['당기순이익']

    else:
        df_pdf['매출액'] = 0
        df_pdf['영업이익'] = 0 
        df_pdf['당기순이익'] = 0 
    return df_pdf

# 재무상태표를 업데이트 하는 함수
def update_dfBS_to_dfpdf(df_pdf):
    # 재무제표에서 해당주식 정보가 준비할 경우 업데이트
    if len(df_need_BS[df_need_BS['종목코드'] == df_pdf['종목코드']])>0:
        df_pdf['유동자산'] = df_need_BS[df_need_BS['종목코드'] ==df_pdf['종목코드']].iloc[-1]['유동자산'] # float()로 묶는 것도 안되면 고려해보자
        df_pdf['자산총계'] = df_need_BS[df_need_BS['종목코드'] == df_pdf['종목코드']].iloc[-1]['자산총계']
        df_pdf['유동부채'] = df_need_BS[df_need_BS['종목코드'] == df_pdf['종목코드']].iloc[-1]['유동부채']
        df_pdf['부채총계']  = df_need_BS[df_need_BS['종목코드'] == df_pdf['종목코드']].iloc[-1]['부채총계']

    else:
        df_pdf['유동자산'] = 0
        df_pdf['자산총계'] = 0 
        df_pdf['유동부채'] = 0 
        df_pdf['부채총계'] = 0
    return df_pdf
     
# 상장 주식수를 업데이트하는 함수
def update_stockamount_to_dfpdf(df_pdf):
    if len(df_stock_amount[df_stock_amount['단축코드'] == df_pdf['종목코드']])>0:
        df_pdf['상장주식수'] = int(df_stock_amount[df_stock_amount['단축코드']==df_pdf['종목코드']]['상장주식수'])
    else:
        df_pdf['상장주식수']  = 0
    return df_pdf
        
        
# 날짜의 범위는 2017년 1월1일부터 2021년 12월 31일까지로 할 예정
# 2017년 1월1일부터 2021년 12월 31일까지로 pdf_files 의 파일들을 일차적으로 거르기(split 활용으로 범위 구하기)
need_pdf_file_list = list()
origin_pdf_file_list = os.listdir('C:\\Users\\LG\\Desktop\\pdf_files')
for origin_pdf_file in origin_pdf_file_list:
    if 20170101<=int(origin_pdf_file.split('.')[0].split('_')[1]) and 20211231>=int(origin_pdf_file.split('.')[0].split('_')[1]):
        need_pdf_file_list.append(origin_pdf_file)


# 주식수를 알기 위해서 after_pdf_kr_stock_list 데이터프레임으로 읽기
df_stock_amount=pd.read_csv("C:\\self_project\\snowball\\Download_data\\after_pdf_kr_stock_list.csv",encoding='cp949')

# 통합 재무상태표 데이터프레임으로 읽기
df_totol_BS=pd.read_csv("C:\\self_project\\snowball\\Download_data\\total_BS.csv",encoding='cp949')
df_totol_BS = df_totol_BS.apply(make_date_to_int, axis=1)
# display(df_totol_BS)


# 통합 손익계산서 데이터프레임으로 읽기
df_totol_PL=pd.read_csv("C:\\self_project\\snowball\\Download_data\\total_PL.csv",encoding='cp949')
df_totol_PL = df_totol_PL.apply(make_date_to_int, axis=1)
# display(df_totol_PL)

# financial 데이터프레임(결과물) df_financial 을 생성(컬럼들은 금융상품코드, pdf 일자, 재무지표들)
df_financial = pd.DataFrame({},columns=['금융상품코드','날짜','추정매출액','추정영업이익','추정당기순이익','추정유동자산','추정자산총계','추정유동부채','추정부채총계'])


# 걸러진 파일들을 모두에 적용(for를 통해) - 각 시점에서 재무지표들 업데이트 할 것! 
for i,need_pdf_file in enumerate(need_pdf_file_list):
    # print(need_pdf_file)
    # pdf파일을 데이터프레임 df_pdf 으로 읽기
    df_pdf = pd.read_csv("C:\\Users\\LG\\Desktop\\pdf_files\\" + need_pdf_file,encoding='cp949')

    df_need_PL = df_totol_PL.copy() # 통합한 손익계산서를 복사해서 수정
    df_need_BS = df_totol_BS.copy() # 통합한 재무상태표를 복사해서 수정
    
    # pdf 파일 날짜에서 가장 가까운(결산기준일과 pdf 날짜 비교) 재무상태표,손익계산서 선택
    df_need_PL['결산기준일차이'] =df_need_PL['결산기준일'] - int(need_pdf_file.split('.')[0].split('_')[1]) # pdf파일 날짜 정수화
    df_need_BS['결산기준일차이'] =df_need_BS['결산기준일'] - int(need_pdf_file.split('.')[0].split('_')[1])
    
    # 재무정보가 주어진 날짜보다 미래의 정보들이면 쓸모가 없으므로 제거
    df_need_PL = df_need_PL.drop(df_need_PL[df_need_PL['결산기준일차이'] > 0].index)
    df_need_BS = df_need_BS.drop(df_need_BS[df_need_BS['결산기준일차이'] > 0].index)
    
    df_need_PL= df_need_PL.apply(add_0_to_stock_code, axis=1) # 종목코드들에 '0'을 붙여서 종목코드 만듬
    df_need_BS= df_need_BS.apply(add_0_to_stock_code, axis=1)
    # 
    df_pdf=df_pdf.apply(update_dfPL_to_dfpdf, axis=1) # 손익계산서의 내용들을 업데이트
    df_pdf=df_pdf.apply(update_dfBS_to_dfpdf, axis=1) # 재무상태표의 내용들을 업데이트
    
    df_pdf=df_pdf.apply(update_stockamount_to_dfpdf, axis=1) # 상장 주식수들을 업데이트
    df_pdf['곱 변수'] = df_pdf['주식수(계약수)'] / df_pdf['상장주식수'] # 전체주식수대비 금융상품이 가지고 있는 주식수의 비율을 구함
    
    # 재무 지표들을 업데이트
    df_pdf['매출액'] = df_pdf['매출액'] * df_pdf['곱 변수']
    df_pdf['영업이익'] = df_pdf['영업이익'] * df_pdf['곱 변수']
    df_pdf['당기순이익'] = df_pdf['당기순이익'] * df_pdf['곱 변수']
    df_pdf['유동자산'] = df_pdf['유동자산'] * df_pdf['곱 변수']
    df_pdf['자산총계'] = df_pdf['자산총계'] * df_pdf['곱 변수']
    df_pdf['유동부채'] = df_pdf['유동부채'] * df_pdf['곱 변수']
    df_pdf['부채총계'] = df_pdf['부채총계'] * df_pdf['곱 변수']
    
    # 사용하지 않을 컬럼들을 삭제
    df_pdf=df_pdf.drop(['종목코드','구성종목명','주식수(계약수)','평가금액','시가총액','시가총액 구성비중','곱 변수','상장주식수'], axis=1)
    df_pdf = df_pdf.replace([np.inf, -np.inf], np.nan) # 값이 무한으로 되어있는 부분은 결측치로 수정
    df_pdf = df_pdf.fillna(0)# 결측치들은 0으로 수정
    df_pdf =df_pdf.sum() # 각 컬럼별 합들을 구함
    new_row = {'금융상품코드':need_pdf_file.split('.')[0].split('_')[0], '날짜':need_pdf_file.split('.')[0].split('_')[1], 
               '추정매출액':df_pdf['매출액'], '추정영업이익':df_pdf['영업이익'],
               '추정당기순이익':df_pdf['당기순이익'],'추정유동자산':df_pdf['유동자산'],
               '추정자산총계':df_pdf['자산총계'],'추정유동부채':df_pdf['유동부채'],'추정부채총계':df_pdf['부채총계']}
    
    df_financial.loc[len(df_financial.index)] = [need_pdf_file.split('.')[0].split('_')[0], need_pdf_file.split('.')[0].split('_')[1], df_pdf['매출액'],
                                                 df_pdf['영업이익'], df_pdf['당기순이익'],df_pdf['유동자산'],df_pdf['자산총계'],df_pdf['유동부채'],df_pdf['부채총계']] 
    #append row to the dataframe
    # print(new_row)
    display(df_financial)
    
    # 재무제표에서 해당주식 정보가 준비할 경우 업데이트
df_financial.to_csv('C:\self_project\snowball\Download_data\\product_financial.csv', index=False,encoding='cp949') 
    # 금융상품의 각 주식들에 각각 주식재무지표들값 * (구성주식수들/주식상장주식수) 해서 새로생성되는 재무지표들을 계산
    
    # df_financial에 행 하나씩 추가
    
# df_financial 정렬 

# df_financial 저장
    