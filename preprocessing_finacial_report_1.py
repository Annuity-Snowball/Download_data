# 재무제표인 txt 파일들 csv 파일로 수정하여 저장하는 코드

import pandas as pd
from IPython.display import display

# 2016년 1분기 재무상태표저장
'''
df_base[df_base['종목코드']=='036260']
df_2016_1Q_BS.loc['036260']['ifrs_CurrentAssets'] = 27741959839
df_2016_1Q_BS.loc['036260']['ifrs_CurrentLiabilities'] = 17355581985
'''

# 2016년 2분기 재무상태표저장
'''          
df_base[df_base['종목코드']=='036260']
df_2016_2Q_BS.loc['036260']['ifrs_CurrentAssets'] = 26949283058
df_2016_2Q_BS.loc['036260']['ifrs_CurrentLiabilities'] = 12126976146
'''

# 2016년 3분기 재무상태표저장
'''
df_base[df_base['종목코드']=='036260']
df_2016_3Q_BS.loc['036260']['ifrs_CurrentAssets'] = 21981347310
df_2016_3Q_BS.loc['036260']['ifrs_CurrentLiabilities'] = 9063062098
'''

# 2016년 4분기 재무상태표저장
'''
df_base[df_base['종목코드']=='036260']
df_2016_4Q_BS.loc['036260']['ifrs_CurrentAssets'] = 24215971739
df_2016_4Q_BS.loc['036260']['ifrs_CurrentLiabilities'] = 6835915654

'''


def make_bs_file():
    # 2016년 부터 for 문으로 실행
    bs_info_list = [
                    ['2016_1Q_BS.txt','당기 1분기말','2016_1Q_BS.csv'],
                    ['2016_2Q_BS.txt','당기 반기말','2016_2Q_BS.csv'],
                    ['2016_3Q_BS.txt','당기 3분기말','2016_3Q_BS.csv'],
                    ['2016_4Q_BS.txt','당기','2016_4Q_BS.csv'],
                    
                    ['2017_1Q_BS.txt','당기 1분기말','2017_1Q_BS.csv'],
                    ['2017_2Q_BS.txt','당기 반기말','2017_2Q_BS.csv'],
                    ['2017_3Q_BS.txt','당기 3분기말','2017_3Q_BS.csv'],
                    ['2017_4Q_BS.txt','당기','2017_4Q_BS.csv'],
                    
                    ['2018_1Q_BS.txt','당기 1분기말','2018_1Q_BS.csv'],
                    ['2018_2Q_BS.txt','당기 반기말','2018_2Q_BS.csv'],
                    ['2018_3Q_BS.txt','당기 3분기말','2018_3Q_BS.csv'],
                    ['2018_4Q_BS.txt','당기','2018_4Q_BS.csv'],
                    
                    ['2019_1Q_BS.txt','당기 1분기말','2019_1Q_BS.csv'],
                    ['2019_2Q_BS.txt','당기 반기말','2019_2Q_BS.csv'],
                    ['2019_3Q_BS.txt','당기 3분기말','2019_3Q_BS.csv'],
                    ['2019_4Q_BS.txt','당기','2019_4Q_BS.csv'],
                    
                    ['2020_1Q_BS.txt','당기 1분기말','2020_1Q_BS.csv'],
                    ['2020_2Q_BS.txt','당기 반기말','2020_2Q_BS.csv'],
                    ['2020_3Q_BS.txt','당기 3분기말','2020_3Q_BS.csv'],
                    ['2020_4Q_BS.txt','당기','2020_4Q_BS.csv'],
                    
                    ['2021_1Q_BS.txt','당기 1분기말','2021_1Q_BS.csv'],
                    ['2021_2Q_BS.txt','당기 반기말','2021_2Q_BS.csv'],
                    ['2021_3Q_BS.txt','당기 3분기말','2021_3Q_BS.csv'],
                    ['2021_4Q_BS.txt','당기','2021_4Q_BS.csv'],
                    
                    ['2022_1Q_BS.txt','당기 1분기말','2022_1Q_BS.csv'],
                    ['2022_2Q_BS.txt','당기 반기말','2022_2Q_BS.csv']
                    ]
    for bs_info in bs_info_list:
        df=pd.read_csv("C:\\Users\\LG\\Desktop\\financial_report\\"+bs_info[0],delimiter="\t", encoding='cp949')
        
        print('df.shape')
        print(df.shape)
        print('df.info()')
        print(df.info())
        print('df.dtypes')
        print(df.dtypes)
        df.head()

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
        current_assets = ['ifrs_CurrentAssets','ifrs-full_CurrentAssets']
        assets = ['ifrs_Assets', 'ifrs-full_Assets']
        current_liabilities = ['ifrs_CurrentLiabilities', 'ifrs-full_CurrentLiabilities']
        liabilities = ['ifrs_Liabilities', 'ifrs-full_Liabilities']
        
        if bs_info[0].split('_')[0] == '2016' or bs_info[0].split('_')[0] == '2017' or bs_info[0].split('_')[0] == '2018' or bs_info[0].split('_')[0] == '2019':
            i=0 #i는 current_assests 등 표현을 위해서 사용되는 변수
        else:
            i=1
        df_basic =df_basic[(df_basic['항목코드'] == current_assets[i])|(df_basic['항목코드'] == assets[i])|(df_basic['항목코드'] == current_liabilities[i])|(df_basic['항목코드'] == liabilities[i])] 
        

        column_list = list(df_basic['항목코드'].unique()) # 결과 데이터프레임의 컬럼들을 설정
        column_list.append('결산기준일') # 컬럼 '결산기준일'dmf cnrk

        # 결과 데이터프레임 생성 = 틀 생성
        df_BS = pd.DataFrame({},columns=column_list, index=df_basic['종목코드'].unique())
        df_BS.index.name = '종목코드' # 데이터프레임의 인덱스명을 설정

        # 결과 데이터프레임의 에 맞는 값들을 할당하는 함수
        def func(df):
            df_BS.loc[df['종목코드']][df['항목코드']]=df[bs_info[1]]
            df_BS.loc[df['종목코드']]['결산기준일']=df['결산기준일']
        df_basic.apply(func,axis=1) # 함수 적용


        # 결과데이터프레임 결측치확인
        check_null_frame = df_BS[df_BS[current_assets[i]].isnull() | df_BS[assets[i]].isnull() | df_BS[current_liabilities[i]].isnull() | df_BS[liabilities[i]].isnull()].copy()
        # print(null_stock_code)

        if len(check_null_frame) >0:
            # 결측치를 매칭하는 함수 부분
            null_dict = dict() # 결측치들의 종목코드와 어떤 지표가 결측치인지 매칭 시키는 딕셔너리 생성
            def func2(df):
                if df.name not in null_dict:   
                    null_dict[df.name] = list(df[df.isnull()==True].index)
            check_null_frame.apply(func2)
            del null_dict['결산기준일'] # 결산기준일은 결측치가 없으므로 제거
            # print(null_dict) # ex) {'ifrs_CurrentAssets': ['000040', '089230', '048770', '036260', '114120', '115160'], 'ifrs_Assets': ['096760', '004990', '095270', '053300', '079430'], 'ifrs_CurrentLiabilities': ['000040', '089230', '048770', '004990', '036260', '115160'], 'ifrs_Liabilities': ['067290', '025000', '004990', '145210', '053300']}




            for null_category in null_dict: # null_dict의 key값들에 대해서 반복
                if null_category == current_assets[i]: # 결측치 카테고리가 'ifrs_CurrentAssets' 일때,
                    category_name_list = ['유동자산','유동 자산']
                elif null_category == assets[i]:
                    category_name_list = ['자산총계','자산 총계']
                elif null_category == current_liabilities[i]:
                    category_name_list = ['유동부채', '유동 부채']
                elif null_category == liabilities[i]:
                    category_name_list = ['부채총계', '부채 총계']
                    
                for null_stock_code in null_dict[null_category]: # 'ifrs_CurrentAssets' 에서 결측치를 가진 '종목코드'들을 추출
                    for category_name in category_name_list:
                        df_temp = df_base[df_base['종목코드']==null_stock_code] # 'ifrs_CurrentAssets' 으로 선택하지 못해서, 항목명으로 정보를 얻기위해 사용
                        df_temp = df_temp[df_temp['항목명'].str.strip() == category_name] # '항목명'이 category_name인 것을 선택
                        if len(df_temp) >0:
                            df_BS.loc[null_stock_code][null_category] = df_temp.loc[df_temp.index[0]][bs_info[1]]




                    
        df_BS.columns = ['유동자산', '자산총계', '유동부채', '부채총계','결산기준일'] # 컬럼명들을 수정
        df_BS = df_BS.reset_index('종목코드') # 인덱스를 컬럼으로 초기화
        df_BS.to_csv('C:\\Users\\LG\\Desktop\\preprocessing_financial\\'+bs_info[2], index=False,encoding='cp949') # 파일로 저장


# 아직 구현 못함...
def make_cf_file():
    # 2016년 부터 for 문으로 실행
    cf_info_list = [
                    ['2016_1Q_CF.txt','당기 1분기','2016_1Q_CF.csv'],
                    ['2016_2Q_CF.txt','당기 반기','2016_2Q_CF.csv'],
                    ['2016_3Q_CF.txt','당기 3분기','2016_3Q_CF.csv'],
                    ['2016_4Q_CF.txt','당기','2016_4Q_CF.csv'],
                    
                    ['2017_1Q_CF.txt','당기 1분기','2017_1Q_CF.csv'],
                    ['2017_2Q_CF.txt','당기 반기','2017_2Q_CF.csv'],
                    ['2017_3Q_CF.txt','당기 3분기','2017_3Q_CF.csv'],
                    ['2017_4Q_Cf.txt','당기','2017_4Q_CF.csv'],
                    
                    ['2018_1Q_CF.txt','당기 1분기','2018_1Q_CF.csv'],
                    ['2018_2Q_CF.txt','당기 반기','2018_2Q_CF.csv'],
                    ['2018_3Q_CF.txt','당기 3분기','2018_3Q_CF.csv'],
                    ['2018_4Q_CF.txt','당기','2018_4Q_CF.csv'],
                    
                    ['2019_1Q_CF.txt','당기 1분기','2019_1Q_CF.csv'],
                    ['2019_2Q_CF.txt','당기 반기','2019_2Q_CF.csv'],
                    ['2019_3Q_CF.txt','당기 3분기','2019_3Q_CF.csv'],
                    ['2019_4Q_CF.txt','당기','2019_4Q_CF.csv'],
                    
                    ['2020_1Q_CF.txt','당기 1분기','2020_1Q_CF.csv'],
                    ['2020_2Q_CF.txt','당기 반기','2020_2Q_CF.csv'],
                    ['2020_3Q_CF.txt','당기 3분기','2020_3Q_CF.csv'],
                    ['2020_4Q_CF.txt','당기','2020_4Q_CF.csv'],
                    
                    ['2021_1Q_CF.txt','당기 1분기','2021_1Q_CF.csv'],
                    ['2021_2Q_CF.txt','당기 반기','2021_2Q_CF.csv'],
                    ['2021_3Q_CF.txt','당기 3분기','2021_3Q_CF.csv'],
                    ['2021_4Q_CF.txt','당기','2021_4Q_CF.csv'],
                    
                    ['2022_1Q_CF.txt','당기 1분기','2022_1Q_CF.csv'],
                    ['2022_2Q_CF.txt','당기 반기','2022_2Q_CF.csv']
                    ]
    for cf_info in cf_info_list:
        df=pd.read_csv("C:\\Users\\LG\\Desktop\\financial_report\\"+cf_info[0],delimiter="\t", encoding='cp949')
        
        print('df.shape')
        print(df.shape)
        print('df.info()')
        print(df.info())
        print('df.dtypes')
        print(df.dtypes)
        df.head()

        def stock_code_preprocessing(df_data):
            stock_code = df_data['종목코드']
            stock_code = stock_code[1:-1]
            df_data['종목코드'] = stock_code
            return df_data

            
        # 가져온 데이터프레임에서 필요한 컬럼명만 추출
        df_base = df.copy() # 불러온 df에 영향을 주지 않기 위해서 copy 사용
        df_base = df_base.apply(stock_code_preprocessing,axis=1) # 종목코드의 [] 을 제거하는 함수 적용, df를 건들지 말고 df_base를 참조

        df_basic = df_base.copy() # df_basic은 필요한 항목콕드에 해당하는 정보들만 추출하기 위해서 사용


        # 2.  현금흐름표에서 영업현금흐름,투자활동현금흐름,재무활동현금흐름 등 필요한 지표들을 항목코드 컬럼을 통해 선택해서 추출
        operating_activity = ['ifrs_CashFlowsFromUsedInOperatingActivities','ifrs-full_CashFlowsFromUsedInOperatingActivities'] # 영업할동현금흐름
        investing_activity = ['ifrs_CashFlowsFromUsedInInvestingActivities', 'ifrs-full_CashFlowsFromUsedInInvestingActivities'] # 투자활동현금흐름
        financing_activity = ['ifrs_CashFlowsFromUsedInFinancingActivities', 'ifrs-full_CashFlowsFromUsedInFinancingActivities'] # 재무활동현금흐름
        
        if cf_info[0].split('_')[0] == '2016' or cf_info[0].split('_')[0] == '2017' or cf_info[0].split('_')[0] == '2018' or cf_info[0].split('_')[0] == '2019':
            i=0 #i는 current_assests 등 표현을 위해서 사용되는 변수
        else:
            i=1
        df_basic =df_basic[(df_basic['항목코드'] == operating_activity[i])|(df_basic['항목코드'] == investing_activity[i])|(df_basic['항목코드'] == financing_activity[i])] 
        

        column_list = list(df_basic['항목코드'].unique()) # 결과 데이터프레임의 컬럼들을 설정
        column_list.append('결산기준일') # 컬럼 '결산기준일'dmf cnrk

        # 결과 데이터프레임 생성 = 틀 생성
        df_CF = pd.DataFrame({},columns=column_list, index=df_basic['종목코드'].unique())
        df_CF.index.name = '종목코드' # 데이터프레임의 인덱스명을 설정

        # 결과 데이터프레임의 에 맞는 값들을 할당하는 함수
        def func(df):
            df_CF.loc[df['종목코드']][df['항목코드']]=df[cf_info[1]]
            df_CF.loc[df['종목코드']]['결산기준일']=df['결산기준일']
        df_basic.apply(func,axis=1) # 함수 적용


        # 결과데이터프레임 결측치확인
        check_null_frame = df_CF[df_CF[operating_activity[i]].isnull() | df_CF[investing_activity[i]].isnull() | df_CF[financing_activity[i]].isnull()].copy()
        # print(null_stock_code)

        if len(check_null_frame) >0:
            # 결측치를 매칭하는 함수 부분
            null_dict = dict() # 결측치들의 종목코드와 어떤 지표가 결측치인지 매칭 시키는 딕셔너리 생성
            def func2(df):
                if df.name not in null_dict:   
                    null_dict[df.name] = list(df[df.isnull()==True].index)
            check_null_frame.apply(func2)
            del null_dict['결산기준일'] # 결산기준일은 결측치가 없으므로 제거
            # print(null_dict) # ex) {'ifrs_CurrentAssets': ['000040', '089230', '048770', '036260', '114120', '115160'], 'ifrs_Assets': ['096760', '004990', '095270', '053300', '079430'], 'ifrs_CurrentLiabilities': ['000040', '089230', '048770', '004990', '036260', '115160'], 'ifrs_Liabilities': ['067290', '025000', '004990', '145210', '053300']}




            for null_category in null_dict: # null_dict의 key값들에 대해서 반복
                category_name_list = list()
                if null_category == operating_activity[i]: # 결측치 카테고리가 'ifrs_CurrentAssets' 일때,
                    category_name_list = ['영업활동으로 인한 현금 흐름', '영업활동 현금흐름'] # 후보들 '영업에서 창출된 현금'
                elif null_category == investing_activity[i]:
                    category_name_list = ['투자활동현금흐름']
                elif null_category == financing_activity[i]:
                    category_name_list = ['재무활동현금흐름']
                
                for null_stock_code in null_dict[null_category]: # 'ifrs_CurrentAssets' 에서 결측치를 가진 '종목코드'들을 추출
                    for category_name in category_name_list:
                        df_temp = df_base[df_base['종목코드']==null_stock_code] # 'ifrs_CurrentAssets' 으로 선택하지 못해서, 항목명으로 정보를 얻기위해 사용
                        df_temp = df_temp[df_temp['항목명'].str.strip() == category_name] # '항목명'이 category_name인 것을 선택
                        if len(df_temp) >0:
                            if df_temp.loc[df_temp.index[0]][cf_info[1]] is not None: # 항목명은 있는데 당기 1분기 값이 null 값이 아닌 경우에 값을 가져와야 함!
                                df_CF.loc[null_stock_code][null_category] = df_temp.loc[df_temp.index[0]][cf_info[1]]




                    
        df_CF.columns = ['유동자산', '자산총계', '유동부채', '부채총계','결산기준일'] # 컬럼명들을 수정
        df_CF = df_CF.reset_index('종목코드') # 인덱스를 컬럼으로 초기화
        df_CF.to_csv('C:\\Users\\LG\\Desktop\\preprocessing_financial\\'+cf_info[2], index=False,encoding='cp949') # 파일로 저장

make_bs_file()
