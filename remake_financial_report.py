# 손익계산서가 누적으로 되어 있으므로 4분기 처럼 계산한후, 
# 손익계산서와 재무상태표 파일들  각각 하나의 통합 파일들로 만드는 코드

import os
import pandas as pd
from IPython.display import display


# 손익계산서의 값들이 str 이어서 float로 변환하는 함수
def PL_type_to_float(df):
    if isinstance(df['매출액'], str):
        if df['매출액'] == '0':
            df['매출액'] = 0
        else:
            if df['매출액'][1] == '-':
                df['매출액'] = df['매출액'][1:] 
            df['매출액'] = float(''.join(df['매출액'].split(',')))
            
    if isinstance(df['영업이익'], str):
        if df['영업이익'] == '0':
            df['영업이익'] = 0
        else:
            if df['영업이익'][1] == '-':
                df['영업이익'] = df['영업이익'][1:] 
            df['영업이익'] = float(''.join(df['영업이익'].split(',')))
        
    if isinstance(df['당기순이익'], str):
        if df['당기순이익'] == '0':
            df['당기순이익'] = 0
        else:
            if df['당기순이익'][1] == '-':
                df['당기순이익'] = df['당기순이익'][1:] 
            df['당기순이익'] = float(''.join(df['당기순이익'].split(',')))
    return df

# 재무상태표의 값들이 str 이어서 float로 변환하는 함수
def BS_type_to_float(df):
    if isinstance(df['유동자산'], str):
        df['유동자산'] = float(''.join(df['유동자산'].split(',')))
    if isinstance(df['자산총계'], str):
        df['자산총계'] = float(''.join(df['자산총계'].split(',')))
    if isinstance(df['유동부채'], str):
        df['유동부채'] = float(''.join(df['유동부채'].split(',')))
    if isinstance(df['부채총계'], str):
        df['부채총계'] = float(''.join(df['부채총계'].split(',')))
        
    return df
    
    

# 통합손익계산서파일 만드는코드
def make_total_PL_report():
    PL_file_list = os.listdir('C:\\Users\\LG\Desktop\\result_PL')
    df_PL_total = pd.DataFrame({},columns=['종목코드','매출액','영업이익','당기순이익','결산기준일'])
    for PL_file_name in PL_file_list:
        df_PL =  pd.read_csv('C:\\Users\\LG\Desktop\\result_PL\\'+PL_file_name, encoding='cp949')
        if PL_file_name.split('_')[1] == '1Q': # 1분기 손익계산서인 경우
            print(PL_file_name)
            display(df_PL)
            df_PL = df_PL.apply(PL_type_to_float, axis=1)
            df_PL['매출액'] = df_PL['매출액']*4
            df_PL['영업이익'] = df_PL['영업이익']*4
            df_PL['당기순이익'] = df_PL['당기순이익']*4
            df_PL_total = pd.concat([df_PL_total, df_PL], axis=0) # 결과 데이터프레임에 통합
            display(df_PL_total)
        elif PL_file_name.split('_')[1] == '2Q': # 2분기 손익계산서인 경우
            print(PL_file_name)
            display(df_PL)
            df_PL = df_PL.apply(PL_type_to_float, axis=1)
            
            df_PL['매출액'] = df_PL['매출액']*2
            df_PL['영업이익'] = df_PL['영업이익']*2
            df_PL['당기순이익'] = df_PL['당기순이익']*2
            df_PL_total = pd.concat([df_PL_total, df_PL], axis=0)
            display(df_PL_total)
            
        elif PL_file_name.split('_')[1] == '3Q': # 3분기 손익계산서인 경우
            print(PL_file_name)
            display(df_PL)
            df_PL = df_PL.apply(PL_type_to_float, axis=1)
            
            df_PL['매출액'] = (df_PL['매출액']/3)*4
            df_PL['영업이익'] = (df_PL['영업이익']/3)*4
            df_PL['당기순이익'] = (df_PL['당기순이익']/3)*4
            df_PL_total = pd.concat([df_PL_total, df_PL], axis=0)
            display(df_PL_total)
            
            
        elif PL_file_name.split('_')[1] == '4Q': # 3분기 손익계산서인 경우
            print(PL_file_name)
            display(df_PL)
            df_PL = df_PL.apply(PL_type_to_float, axis=1)
            df_PL_total = pd.concat([df_PL_total, df_PL], axis=0)
            display(df_PL_total)
    df_PL_total.to_csv('C:\\self_project\\snowball\\Download_data\\total_PL.csv', index=False,encoding='cp949') # 파일로 저장
    
    
    
# 통합재무상태표 만드는 코드
def make_total_BS_report():
    BS_file_list = os.listdir('C:\\Users\\LG\Desktop\\result_BS')
    df_BS_total = pd.DataFrame({},columns=['종목코드','유동자산','자산총계','유동부채','부채총계','결산기준일'])
    for BS_file_name in BS_file_list:  
        print(BS_file_name) 
        df_BS =  pd.read_csv('C:\\Users\\LG\Desktop\\result_BS\\'+BS_file_name, encoding='cp949')
        display(df_BS)
        df_BS = df_BS.apply(BS_type_to_float, axis=1)
        df_BS_total = pd.concat([df_BS_total, df_BS], axis=0) # 결과 데이터프레임에 통합
        display(df_BS_total)
        print()
    df_BS_total.to_csv('C:\\self_project\\snowball\\Download_data\\total_BS.csv', index=False,encoding='cp949') # 파일로 저장

# make_total_PL_report()
# make_total_BS_report()
