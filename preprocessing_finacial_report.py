# 재무제표인 txt 파일들 csv 파일로 수정하여 저장하는 코드

import pandas as pd

'''
# 여기서부터
file = open("C:\\Users\\LG\\Desktop\\financial_report\\2016_1Q_BS.txt", "r")

file_rows = file.readlines() # 텍스트파일의 행들을 한 줄씩 읽어서 리스트로 저장
# print(file_rows[1].split('\t'))
df = pd.DataFrame({},columns=file_rows[0].split('\t')[:-1]) # 주식의 재무제표를 저장할 데이터프레옴

# print(len(file_rows))
for i, file_row in enumerate(file_rows[1:]):
    file_row = file_row.split('\t')
    print(i)
    df.loc[i] = file_row
file.close()
print('df.shape')
print(df.shape)
print('df.info()')
print(df.info())
print('df.dtypes')
print(df.dtypes)
df.head()
# 여기까지는 한번만실행, ㅈㄴ 오래걸림 - 16분 걸림

########################################################################
# 향후 코드 실행

def stock_code_preprocessing(df_data):
    stock_code = df_data['종목코드']
    stock_code = stock_code[1:-1]
    df_data['종목코드'] = stock_code
    return df_data

    
    
    
# 가져온 데이터프레임에서 필요한 컬럼명만 추출
df_base = df.copy() # 불러온 df에 영향을 주지 않기 위해서 copy 사용
df_base = df_base.apply(stock_code_preprocessing,axis=1) # 종목코드의 [] 을 제거하는 함수 적용, df를 건들지 말고 df_base를 참조

df_basic = df_base.copy() # df_basic은 필요한 항목콕드에 해당하는 정보들만 추출하기 위해서 사용

# 1. 항목코드와 항목명들 매칭 확인하기 위해서 csv 파일로 저장해서 확인
# df_basic.to_csv("C:\self_project\snowball\Download_data\\stock_code_info1.csv",index=False,encoding="utf-8-sig") 

# 2. 20161Q 대차대조표에서 유동자산, 비유동자산 등 필요한 지표들을 항목코드 컬럼을 통해 선택해서 추출
df_basic =df_basic[(df_basic['항목코드'] == 'ifrs_CurrentAssets')|(df_basic['항목코드'] == 'ifrs_Assets')|(df_basic['항목코드'] == 'ifrs_CurrentLiabilities')|(df_basic['항목코드'] == 'ifrs_Liabilities')] 

column_list = list(df_basic['항목코드'].unique()) # 결과 데이터프레임의 컬럼들을 설정
column_list.append('결산기준일') # 컬럼 '결산기준일'dmf cnrk

# 결과 데이터프레임 생성 = 틀 생성
df_2016_1Q_BS = pd.DataFrame({},columns=column_list, index=df_basic['종목코드'].unique())
df_2016_1Q_BS.index.name = '종목코드' # 데이터프레임의 인덱스명을 설정

# 결과 데이터프레임의 에 맞는 값들을 할당하는 함수
def func(df):
    df_2016_1Q_BS.loc[df['종목코드']][df['항목코드']]=df['당기 1분기말']
    df_2016_1Q_BS.loc[df['종목코드']]['결산기준일']=df['결산기준일']
df_basic.apply(func,axis=1) # 함수 적용

# 결과데이터프레임 결측치확인
# check_null_frame = df_2016_1Q_BS[df_2016_1Q_BS['ifrs_CurrentAssets'].isnull() | df_2016_1Q_BS['ifrs_Assets'].isnull() | df_2016_1Q_BS['ifrs_CurrentLiabilities'].isnull() | df_2016_1Q_BS['ifrs_Liabilities'].isnull()].copy()
# print(check_null_frame)

# 2016_1Q_BS 결측치 채우는 코드! - 한번만 실행 (결측치가 있는 종목 코드들 : '067290', '096760', '025000', '000040', '004990', '065710', '145210','089230', '095270', '036260', '114120', '053300', '009240', '079430','115160')
# 더 최적화해서 코드 구현 필요
df_base[df_base['종목코드']=='067290'] # 결측치에 어떤 값을 넣어야 하는지 확인위해서 조회 필요!
df_2016_1Q_BS.loc['067290']['ifrs_Liabilities'] = df_base.loc[1636]['당기 1분기말'] # 결측치 채우기 진행

df_base[df_base['종목코드']=='096760']
df_2016_1Q_BS.loc['096760']['ifrs_Assets'] = df_base.loc[1714]['당기 1분기말']

df_base[df_base['종목코드']=='025000']
df_2016_1Q_BS.loc['025000']['ifrs_Liabilities'] = df_base.loc[2509]['당기 1분기말']

df_base[df_base['종목코드']=='000040']
df_2016_1Q_BS.loc['000040']['ifrs_CurrentAssets'] = df_base.loc[2583]['당기 1분기말']
df_2016_1Q_BS.loc['000040']['ifrs_CurrentLiabilities'] = df_base.loc[2597]['당기 1분기말']

df_base[df_base['종목코드']=='004990']
df_2016_1Q_BS.loc['004990']['ifrs_Assets'] = df_base.loc[18479]['당기 1분기말']
df_2016_1Q_BS.loc['004990']['ifrs_CurrentLiabilities'] = df_base.loc[18481]['당기 1분기말']
df_2016_1Q_BS.loc['004990']['ifrs_Liabilities'] = df_base.loc[18499]['당기 1분기말']

df_base[df_base['종목코드']=='065710']
df_2016_1Q_BS.loc['065710']['ifrs_CurrentAssets'] = df_base.loc[25885]['당기 1분기말']
df_2016_1Q_BS.loc['065710']['ifrs_CurrentLiabilities'] = df_base.loc[25935]['당기 1분기말']

df_base[df_base['종목코드']=='145210']
df_2016_1Q_BS.loc['145210']['ifrs_Liabilities'] = df_base.loc[27986]['당기 1분기말']

df_base[df_base['종목코드']=='089230']
df_2016_1Q_BS.loc['089230']['ifrs_CurrentAssets'] = df_base.loc[39206]['당기 1분기말']
df_2016_1Q_BS.loc['089230']['ifrs_CurrentLiabilities'] = df_base.loc[39224]['당기 1분기말']

df_base[df_base['종목코드']=='095270']
df_2016_1Q_BS.loc['095270']['ifrs_Assets'] = df_base.loc[40951]['당기 1분기말']

df_base[df_base['종목코드']=='036260']
df_2016_1Q_BS.loc['036260']['ifrs_CurrentAssets'] = 27741959839
df_2016_1Q_BS.loc['036260']['ifrs_CurrentLiabilities'] = 17355581985

df_base[df_base['종목코드']=='114120']
df_2016_1Q_BS.loc['114120']['ifrs_CurrentAssets'] = df_base.loc[52603]['당기 1분기말']

df_base[df_base['종목코드']=='053300']
df_2016_1Q_BS.loc['053300']['ifrs_Assets'] = df_base.loc[58204]['당기 1분기말']
df_2016_1Q_BS.loc['053300']['ifrs_Liabilities'] = df_base.loc[58221]['당기 1분기말']

df_base[df_base['종목코드']=='009240']
df_2016_1Q_BS.loc['009240']['ifrs_Assets'] = df_base.loc[59274]['당기 1분기말']

df_base[df_base['종목코드']=='079430']
df_2016_1Q_BS.loc['079430']['ifrs_Assets'] = df_base.loc[61835]['당기 1분기말']

df_base[df_base['종목코드']=='115160']
df_2016_1Q_BS.loc['115160']['ifrs_CurrentAssets'] = df_base.loc[63684]['당기 1분기말']
df_2016_1Q_BS.loc['115160']['ifrs_CurrentLiabilities'] = df_base.loc[63701]['당기 1분기말']

# 결측치 처리후 결과데이터프레임 결측치확인
check_null_frame = df_2016_1Q_BS[df_2016_1Q_BS['ifrs_CurrentAssets'].isnull() | df_2016_1Q_BS['ifrs_Assets'].isnull() | df_2016_1Q_BS['ifrs_CurrentLiabilities'].isnull() | df_2016_1Q_BS['ifrs_Liabilities'].isnull()].copy()
# check_null_frame

df_2016_1Q_BS.columns = ['유동자산', '자산총계', '유동부채', '부채총계','결산기준일'] # 컬럼명들을 수정
df_2016_1Q_BS = df_2016_1Q_BS.reset_index('종목코드') # 인덱스를 컬럼으로 초기화
df_2016_1Q_BS.to_csv('C:\\Users\\LG\\Desktop\\result\\2016_1Q_BS.csv', index=False,encoding='cp949') # 파일로 저장
'''

file = open("C:\\Users\\LG\\Desktop\\financial_report\\2016_2Q_BS.txt", "r")

file_rows = file.readlines() # 텍스트파일의 행들을 한 줄씩 읽어서 리스트로 저장
# print(file_rows[1].split('\t'))
df = pd.DataFrame({},columns=file_rows[0].split('\t')[:-1]) # 주식의 재무제표를 저장할 데이터프레옴

# print(len(file_rows))
for i, file_row in enumerate(file_rows[1:]):
    file_row = file_row.split('\t')
    print(i)
    df.loc[i] = file_row
file.close()
print('df.shape')
print(df.shape)
print('df.info()')
print(df.info())
print('df.dtypes')
print(df.dtypes)
df.head()


#################### 여기서 부터 코드 실행
def stock_code_preprocessing(df_data):
    stock_code = df_data['종목코드']
    stock_code = stock_code[1:-1]
    df_data['종목코드'] = stock_code
    return df_data

    
    
    
# 가져온 데이터프레임에서 필요한 컬럼명만 추출
df_base = df.copy() # 불러온 df에 영향을 주지 않기 위해서 copy 사용
df_base = df_base.apply(stock_code_preprocessing,axis=1) # 종목코드의 [] 을 제거하는 함수 적용, df를 건들지 말고 df_base를 참조

df_basic = df_base.copy() # df_basic은 필요한 항목콕드에 해당하는 정보들만 추출하기 위해서 사용

# 1. 항목코드와 항목명들 매칭 확인하기 위해서 csv 파일로 저장해서 확인
# df_basic.to_csv("C:\self_project\snowball\Download_data\\stock_code_info1.csv",index=False,encoding="utf-8-sig") 

# 2. 20161Q 대차대조표에서 유동자산, 비유동자산 등 필요한 지표들을 항목코드 컬럼을 통해 선택해서 추출
df_basic =df_basic[(df_basic['항목코드'] == 'ifrs_CurrentAssets')|(df_basic['항목코드'] == 'ifrs_Assets')|(df_basic['항목코드'] == 'ifrs_CurrentLiabilities')|(df_basic['항목코드'] == 'ifrs_Liabilities')] 

column_list = list(df_basic['항목코드'].unique()) # 결과 데이터프레임의 컬럼들을 설정
column_list.append('결산기준일') # 컬럼 '결산기준일'dmf cnrk

# 결과 데이터프레임 생성 = 틀 생성
df_2016_2Q_BS = pd.DataFrame({},columns=column_list, index=df_basic['종목코드'].unique())
df_2016_2Q_BS.index.name = '종목코드' # 데이터프레임의 인덱스명을 설정

# 결과 데이터프레임의 에 맞는 값들을 할당하는 함수
def func(df):
    df_2016_2Q_BS.loc[df['종목코드']][df['항목코드']]=df['당기 반기말']
    df_2016_2Q_BS.loc[df['종목코드']]['결산기준일']=df['결산기준일']
df_basic.apply(func,axis=1) # 함수 적용


# 결과데이터프레임 결측치확인
check_null_frame = df_2016_2Q_BS[df_2016_2Q_BS['ifrs_CurrentAssets'].isnull() | df_2016_2Q_BS['ifrs_Assets'].isnull() | df_2016_2Q_BS['ifrs_CurrentLiabilities'].isnull() | df_2016_2Q_BS['ifrs_Liabilities'].isnull()].copy()
# print(null_stock_code)

# 결측치를 매칭하는 함수 부분
null_dict = dict() # 결측치들의 종목코드와 어떤 지표가 결측치인지 매칭 시키는 딕셔너리 생성
def func2(df):
    if df.name not in null_dict:   
        null_dict[df.name] = list(df[df.isnull()==True].index)
check_null_frame.apply(func2)
del null_dict['결산기준일'] # 결산기준일은 결측치가 없으므로 제거
print(null_dict) # ex) {'ifrs_CurrentAssets': ['000040', '089230', '048770', '036260', '114120', '115160'], 'ifrs_Assets': ['096760', '004990', '095270', '053300', '079430'], 'ifrs_CurrentLiabilities': ['000040', '089230', '048770', '004990', '036260', '115160'], 'ifrs_Liabilities': ['067290', '025000', '004990', '145210', '053300']}




for null_category in null_dict: # null_dict의 key값들에 대해서 반복
    if null_category == 'ifrs_CurrentAssets': # 결측치 카테고리가 'ifrs_CurrentAssets' 일때,
        category_name = '유동자산'
            
    elif null_category == 'ifrs_Assets':
        category_name = '자산총계'
    elif null_category == 'ifrs_CurrentLiabilities':
        category_name = '유동부채'
    elif null_category == 'ifrs_Liabilities':
        category_name = '부채총계'
        
    for null_stock_code in null_dict[null_category]: # 'ifrs_CurrentAssets' 에서 결측치를 가진 '종목코드'들을 추출
            df_temp = df_base[df_base['종목코드']==null_stock_code] # 'ifrs_CurrentAssets' 으로 선택하지 못해서, 항목명으로 정보를 얻기위해 사용
            df_temp = df_temp[df_temp['항목명'].str.strip() ==category_name] # '항목명'이 category_name인 것을 선택
            if len(list(df_temp['당기 반기말']))>0: # 항목명 category_name으로 값이 선택이 되었을 때
                temp_price = list(df_temp['당기 반기말'])[0] # 금액을 추출하고
                df_2016_2Q_BS.loc[null_stock_code][null_category] = temp_price # 결측치 대신에 값을 할당
            else: # 항목명 '유동자산'으로 값이 선택이 되지 못했을 때
                pass


