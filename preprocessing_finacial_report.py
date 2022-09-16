# 재무제표인 txt 파일들 csv 파일로 수정하여 저장하는 코드

import pandas as pd
from IPython.display import display
import csv

pdf_stock_list = list() # pdf에서 사용되는 종목코드들이 담겨 있는 리스트 생성
with open('C:\\self_project\\snowball\\Download_data\\pdf_stock_list.csv', newline='', encoding='utf-8') as csvfile:
    pre_pdf_stock_list = list(csv.reader(csvfile, delimiter=' ')) # need_stock_list.csv 파일에서 종목코드들을 불러옴


for pdf_stock_code in pre_pdf_stock_list:
    pdf_stock_list.append(pdf_stock_code[0]) # 불러온 종목코드가 각각 리스트로 되어 있으므로, 문자열로 바꾸어 주는 부분이 필요 함!
    

# 대차대조표 만드는 함수
def make_BS_file():
    # 2016년 부터 for 문으로 실행
    BS_info_list = [
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
                    ['2021_4Q_BS.txt','당기','2021_4Q_BS.csv']
                    ]
    for BS_info in BS_info_list:
        print("start :",BS_info[0])
        df=pd.read_csv("C:\\Users\\LG\\Desktop\\report_BS\\"+BS_info[0],delimiter="\t", encoding='cp949')
        

        def stock_code_preprocessing(df_data):
            stock_code = df_data['종목코드']
            stock_code = stock_code[1:-1]
            df_data['종목코드'] = stock_code
            return df_data

            
        # 가져온 데이터프레임에서 필요한 컬럼명만 추출
        df_base = df.copy() # 불러온 df에 영향을 주지 않기 위해서 copy 사용
        df_base = df_base.apply(stock_code_preprocessing,axis=1) # 종목코드의 [] 을 제거하는 함수 적용, df를 건들지 말고 df_base를 참조

    
        df_base = df_base.drop(df_base[~df_base['종목코드'].isin(pdf_stock_list)].index) # 재무제표의 종목코드가 pdf_stock_list 의 종목코드에 없으면 고려할 필요가 없으므로 제거!
                                                                                        # df_base은 pdf_stock_list 에 해당하는 주식의 재무정보들을 담은 데이터프레임
      

        # 2. 20161Q 대차대조표에서 유동자산, 비유동자산 등 필요한 지표들을 항목코드 컬럼을 통해 선택해서 추출
        current_assets = ['ifrs_CurrentAssets','ifrs-full_CurrentAssets']
        assets = ['ifrs_Assets', 'ifrs-full_Assets']
        current_liabilities = ['ifrs_CurrentLiabilities', 'ifrs-full_CurrentLiabilities']
        liabilities = ['ifrs_Liabilities', 'ifrs-full_Liabilities']
        


        column_list = ['CurrentAssets','Assets','CurrentLiabilities','Liabilities','결산기준일']

        # 결과 데이터프레임 생성 = 틀 생성
        df_BS = pd.DataFrame({},columns=column_list, index=df_base['종목코드'].unique())
        df_BS.index.name = '종목코드' # 데이터프레임의 인덱스명을 설정

        # 결과 데이터프레임(df_BS) 에 맞는 값들을 할당하는 함수
        def func(df):
            if df['항목코드'] in current_assets: # 받아온 데이터프레임의 '항목코드' 컬럼이 current_assets 리스트에 있으면
                df_BS.loc[df['종목코드']]['CurrentAssets']=df[BS_info[1]] # df_BS에 업데이트
            elif df['항목코드'] in assets:
                df_BS.loc[df['종목코드']]['Assets']=df[BS_info[1]]
            elif df['항목코드'] in current_liabilities:
                df_BS.loc[df['종목코드']]['CurrentLiabilities']=df[BS_info[1]]           
            elif df['항목코드'] in liabilities:
                df_BS.loc[df['종목코드']]['Liabilities']=df[BS_info[1]]
            df_BS.loc[df['종목코드']]['결산기준일']=df['결산기준일']
        df_base.apply(func,axis=1) # 함수 적용

    # 결과데이터프레임 결측치확인
        check_null_frame = df_BS[df_BS['CurrentAssets'].isnull() | df_BS['Assets'].isnull() | df_BS['CurrentLiabilities'].isnull() | df_BS['Liabilities'].isnull() | df_BS['결산기준일'].isnull()].copy()
    

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
                    if null_category == 'CurrentAssets': # 결측치 카테고리가 'ifrs_CurrentAssets' 일때,
                        category_name_list = ['유동자산','유동 자산','유동자산 합계','I. 유동자산','유동자산합계']
                    elif null_category == 'Assets':
                        category_name_list = ['자산총계','자산 총계','자본과부채총계']
                    elif null_category == 'CurrentLiabilities':
                        category_name_list = ['유동부채', '유동 부채','유동부채 합계', 'I. 유동부채','유동부채합계']
                    elif null_category == 'Liabilities':
                        category_name_list = ['부채총계', '부채 총계']
                        
                    for null_stock_code in null_dict[null_category]: # 'ifrs_CurrentAssets' 에서 결측치를 가진 '종목코드'들을 추출
                        for category_name in category_name_list:
                            df_temp = df_base[df_base['종목코드']==null_stock_code] # 'ifrs_CurrentAssets' 으로 선택하지 못해서, 항목명으로 정보를 얻기위해 사용
                            df_temp = df_temp[df_temp['항목명'].str.strip() == category_name] # '항목명'이 category_name인 것을 선택
                            if len(df_temp) >0:
                                df_BS.loc[null_stock_code][null_category] = df_temp.loc[df_temp.index[0]][BS_info[1]]



        check_null_frame = df_BS[df_BS['CurrentAssets'].isnull() | df_BS['Assets'].isnull() | df_BS['CurrentLiabilities'].isnull() | df_BS['Liabilities'].isnull() | df_BS['결산기준일'].isnull()].copy()
    
        display(check_null_frame)            
        df_BS.columns = ['유동자산', '자산총계', '유동부채', '부채총계','결산기준일'] # 컬럼명들을 수정
        df_BS = df_BS.reset_index('종목코드') # 인덱스를 컬럼으로 초기화
        df_BS.to_csv('C:\\Users\\LG\\Desktop\\result_BS\\'+BS_info[2], index=False,encoding='cp949') # 파일로 저장
        print("end :",BS_info[0])



# 손익계산서 만드는 함수 - 추후에 함수로 덮어야 함!
def make_PL_file():
    # 2016년 부터 for 문으로 실행  - 1분기 누적, 혹은 누적로 할 지 결정해야 함, 4Q는 당기 만 즉 당기누적만 제공함...
    PL_info_list = [
                ['당기 1분기 누적','2016_1Q_PL.csv'],
                ['당기 반기 누적','2016_2Q_PL.csv'],
                ['당기 3분기 누적','2016_3Q_PL.csv'],
                ['당기','2016_4Q_PL.csv'],
                
                ['당기 1분기 누적','2017_1Q_PL.csv'],
                ['당기 반기 누적','2017_2Q_PL.csv'],
                ['당기 3분기 누적','2017_3Q_PL.csv'],
                ['당기','2017_4Q_PL.csv'],
                
                ['당기 1분기 누적','2018_1Q_PL.csv'],
                ['당기 반기 누적','2018_2Q_PL.csv'],
                ['당기 3분기 누적','2018_3Q_PL.csv'],
                ['당기','2018_4Q_PL.csv'],
                
                ['당기 1분기 누적','2019_1Q_PL.csv'],
                ['당기 반기 누적','2019_2Q_PL.csv'],
                ['당기 3분기 누적','2019_3Q_PL.csv'],
                ['당기','2019_4Q_PL.csv'],
                
                ['당기 1분기 누적','2020_1Q_PL.csv'],
                ['당기 반기 누적','2020_2Q_PL.csv'],
                ['당기 3분기 누적','2020_3Q_PL.csv'],
                ['당기','2020_4Q_PL.csv'],
                
                ['당기 1분기 누적','2021_1Q_PL.csv'],
                ['당기 반기 누적','2021_2Q_PL.csv'],
                ['당기 3분기 누적','2021_3Q_PL.csv'],
                ['당기','2021_4Q_PL.csv']
                ]
    for PL_info in PL_info_list:
        print("start :",PL_info[1])
        df=pd.read_csv("C:\\Users\\LG\\Desktop\\after_report_PL\\"+PL_info[1], encoding='cp949')
        

        def stock_code_preprocessing(df_data):
            stock_code = df_data['종목코드']
            stock_code = stock_code[1:-1]
            df_data['종목코드'] = stock_code
            return df_data

            
        # 가져온 데이터프레임에서 필요한 컬럼명만 추출
        df_base = df.copy() # 불러온 df에 영향을 주지 않기 위해서 copy 사용
        df_base = df_base.apply(stock_code_preprocessing,axis=1) # 종목코드의 [] 을 제거하는 함수 적용, df를 건들지 말고 df_base를 참조


        df_base = df_base.drop(df_base[~df_base['종목코드'].isin(pdf_stock_list)].index) # 재무제표의 종목코드가 pdf_stock_list 의 종목코드에 없으면 고려할 필요가 없으므로 제거!
                                                                                        # df_base은 pdf_stock_list 에 해당하는 주식의 재무정보들을 담은 데이터프레임
        

        # 2. 20161Q 대차대조표에서 유동자산, 비유동자산 등 필요한 지표들을 항목코드 컬럼을 통해 선택해서 추출
        revenue = ['ifrs_Revenue','ifrs-full_Revenue'] # 매출
        operating_incomeloss = ['dart_OperatingIncomeLoss'] # 영업이익
        profitloss = ['ifrs_ProfitLoss', 'ifrs-full_ProfitLoss'] # 순이익
        


        column_list = ['Revenue','OperatingIncomeLoss','ProfitLoss','결산기준일']

        # 결과 데이터프레임 생성 = 틀 생성
        df_PL = pd.DataFrame({},columns=column_list, index=df_base['종목코드'].unique())
        df_PL.index.name = '종목코드' # 데이터프레임의 인덱스명을 설정

        # 결과 데이터프레임(df_PL) 에 맞는 값들을 할당하는 함수
        def func(df):
            if df['항목코드'] in revenue: # 받아온 데이터프레임의 '항목코드' 컬럼이 revenue 리스트에 있으면
                df_PL.loc[df['종목코드']]['Revenue']=df[PL_info[0]] # df_PL에 업데이트
            elif df['항목코드'] in operating_incomeloss:
                df_PL.loc[df['종목코드']]['OperatingIncomeLoss']=df[PL_info[0]]           
            elif df['항목코드'] in profitloss:
                df_PL.loc[df['종목코드']]['ProfitLoss']=df[PL_info[0]]
            df_PL.loc[df['종목코드']]['결산기준일']=df['결산기준일']
        df_base.apply(func,axis=1) # 함수 적용

        # 결과데이터프레임 결측치확인
        check_null_frame = df_PL[df_PL['Revenue'].isnull() | df_PL['OperatingIncomeLoss'].isnull() | df_PL['ProfitLoss'].isnull() | df_PL['결산기준일'].isnull()].copy()


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
                if null_category == 'Revenue': # 결측치 카테고리가 'ifrs_CurrentAssets' 일때,
                    # 가능한 항목명들의 리스트들
                    category_name_list = ['매출액','영업수익','매출','영업수익(매출)','Ⅰ. 영업수익','매출과 지분법손익(영업수익)', 
                                          'Ⅰ.매출액','영업수익(매출과지분법손익)','I.매출액','수익','영업수익(매출액','영업수익(매출액)',
                                          'I. 영업수익','매출액 및 지분법손익','I.영업수익']
                elif null_category == 'OperatingIncomeLoss':
                    category_name_list = ['영업이익','영업이익(손실)','영업이익 (손실)', '영업손익', 
                                          '영업 이익', 'Ⅲ. 영업이익', 'Ⅴ.영업이익', '영업손실','Ⅴ.영업이익(손실)','IV.영업이익(손실)']
                elif null_category == 'ProfitLoss':
                    category_name_list = ['당기순이익', '연결당기순이익', '당기연결순이익', '당기순이익(손실)', 
                                          'VI. 당기순이익(손실)', '당기순손익','Ⅷ.당기순이익(손실)','분기순이익',
                                          '연결당기순이익(손실)','당기순손실','당기 순이익','Ⅴ. 당기순이익', '반기순이익',
                                          '연결당기순손실', 'I.당기순이익', '분기연결순이익(손실)','분기순손익','Ⅴ. 반기순이익',
                                          '반기순손익','반기 순이익']
                    
                for null_stock_code in null_dict[null_category]: # 'ifrs_CurrentAssets' 에서 결측치를 가진 '종목코드'들을 추출
                    for category_name in category_name_list:
                        df_temp = df_base[df_base['종목코드']==null_stock_code] # 'ifrs_CurrentAssets' 으로 선택하지 못해서, 항목명으로 정보를 얻기위해 사용
                        df_temp = df_temp[df_temp['항목명'].str.strip() == category_name] # '항목명'이 category_name인 것을 선택
                        if len(df_temp) >0:
                            if category_name == '영업손실':
                                df_PL.loc[null_stock_code][null_category] = '-'+df_temp.loc[df_temp.index[0]][PL_info[0]]
                            else:
                                df_PL.loc[null_stock_code][null_category] = df_temp.loc[df_temp.index[0]][PL_info[0]]




        check_null_frame = df_PL[df_PL['Revenue'].isnull() | df_PL['OperatingIncomeLoss'].isnull() | df_PL['ProfitLoss'].isnull() | df_PL['결산기준일'].isnull()].copy()
        display(check_null_frame)   # 결측치 확인
        df_PL.columns = ['매출액','영업이익','당기순이익','결산기준일'] # 컬럼명들을 수정
        df_PL = df_PL.reset_index('종목코드') # 인덱스를 컬럼으로 초기화
        df_PL.to_csv('C:\\Users\\LG\\Desktop\\result_PL\\'+PL_info[1], index=False,encoding='cp949') # 파일로 저장

   
# 재무상태표 결측치 1차적으로 처리하는 함수
def modify_BS_file_1():
    BS_info_list = [['2016_1Q_BS.txt','당기 1분기말','2016_1Q_BS.csv'],
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
                    ['2021_4Q_BS.txt','당기','2021_4Q_BS.csv']
                    ]
    for BS_info in BS_info_list:
    # 파일에 따라서 BS_info 수정

        print('start :',BS_info[2])
        df=pd.read_csv("C:\\Users\\LG\\Desktop\\report_BS\\"+BS_info[0],delimiter="\t", encoding='cp949')

        df_BS = pd.read_csv("C:\\Users\\LG\\Desktop\\result_BS\\"+BS_info[2], encoding='cp949')

        def stock_code_preprocessing(df_data):
            stock_code = df_data['종목코드']
            stock_code = stock_code[1:-1]
            df_data['종목코드'] = stock_code
            return df_data

            
        # 가져온 데이터프레임에서 필요한 컬럼명만 추출
        df_txt = df.copy() # 불러온 df에 영향을 주지 않기 위해서 copy 사용
        df_txt = df_txt.apply(stock_code_preprocessing,axis=1) 

        df_BS=df_BS.set_index('종목코드')
        
        # 다음은 항목코드의 경우의 수들을 리스트로 표시
        current_assets = ['ifrs_CurrentAssets','ifrs-full_CurrentAssets'] # 유동자산
        assets = ['ifrs_Assets', 'ifrs-full_Assets'] # 자산총계
        current_liabilities = ['ifrs_CurrentLiabilities', 'ifrs-full_CurrentLiabilities'] # 유동부채
        liabilities = ['ifrs_Liabilities', 'ifrs-full_Liabilities'] # 부채총계
        non_current_assets = ['ifrs_NoncurrentAssets','ifrs-full_NoncurrentAssets'] # 비유동자산(8700 회사가 항목코드에 걸리지 않기에 인덱스 범위를 통해서 계산을 해주는 과정 필요)
        non_current_liabilities = ['ifrs_NoncurrentLiabilities', 'ifrs-full_NoncurrentLiabilities']# 비유동부채(8700 회사가 항목코드에 걸리지 않기에 인덱스 범위를 통해서 계산을 해주는 과정 필요)
        
        CurrentAssets_index = list(df_txt[(df_txt['종목코드'] == '008700') & (df_txt['항목코드'].isin(current_assets))].index)[0] # 유동자산의 인덱스 번호를 구함
        NonCurrentAssests_index = list(df_txt[(df_txt['종목코드'] == '008700') & (df_txt['항목코드'].isin(non_current_assets))].index)[0]  # 비유동자산의 인덱스 번호를 구함
        
        CurrentLiabilities_index = list(df_txt[(df_txt['종목코드'] == '008700') & (df_txt['항목코드'].isin(current_liabilities))].index)[0]  # 유동부채의 인덱스 번호를 구함
        NonCurrentLiabilities_index = list(df_txt[(df_txt['종목코드'] == '008700') & (df_txt['항목코드'].isin(non_current_liabilities))].index)[0]   # 비유동부채의 인덱스 번호를 구함
        
        CurrentAssets =0 # 유동자산 금액을 초기화
        CurrentLiabilities =0 # 유동부채 금액을 초기화
        
        # 유동자산과 비유동자산의 인덱스 사이에 있는 모든 항목들을 더하여서 유동자산 구함 - 2016 2Q 8700 중간에 null 이 있어서 오류가 뜸
        for index in range(CurrentAssets_index+1,NonCurrentAssests_index):
            CurrentAssets+=int(''.join(df_txt.loc[index][BS_info[1]].split(',')))
            
        # 유동부채과 비유동부채의 인덱스 사이에 있는 모든 항목들을 더하여서 유동자산 구함
        for index in range(CurrentLiabilities_index+1,NonCurrentLiabilities_index):
            CurrentLiabilities+=int(''.join(df_txt.loc[index][BS_info[1]].split(',')))
        
        # 계산한 금액들 업데이트
        df_BS.loc[8700]['유동자산'] =CurrentAssets
        df_BS.loc[8700]['유동부채'] =CurrentLiabilities
        
        check_null_frame = df_BS[df_BS['유동자산'].isnull() | df_BS['자산총계'].isnull() | df_BS['유동부채'].isnull() | df_BS['부채총계'].isnull() | df_BS['결산기준일'].isnull()].copy()

        display(check_null_frame)
        
        df_BS = df_BS.reset_index('종목코드') # 인덱스를 컬럼으로 초기화
        
        # 수정한 것 파일로 저장
        df_BS.to_csv('C:\\Users\\LG\\Desktop\\result_BS\\'+BS_info[2], index=False,encoding='cp949') # 파일로 저장
        
# 손익계산서 결측치 1차적으로 처리하는 함수
def modify_PL_file_1():  
    PL_info_list = [
                    ['당기 1분기 누적','2016_1Q_PL.csv'],
                    ['당기 반기 누적','2016_2Q_PL.csv'],
                    ['당기 3분기 누적','2016_3Q_PL.csv'],
                    ['당기','2016_4Q_PL.csv'],
                    
                    ['당기 1분기 누적','2017_1Q_PL.csv'],
                    ['당기 반기 누적','2017_2Q_PL.csv'],
                    ['당기 3분기 누적','2017_3Q_PL.csv'],
                    ['당기','2017_4Q_PL.csv'],
                    
                    ['당기 1분기 누적','2018_1Q_PL.csv'],
                    ['당기 반기 누적','2018_2Q_PL.csv'],
                    ['당기 3분기 누적','2018_3Q_PL.csv'],
                    ['당기','2018_4Q_PL.csv'],
                    
                    ['당기 1분기 누적','2019_1Q_PL.csv'],
                    ['당기 반기 누적','2019_2Q_PL.csv'],
                    ['당기 3분기 누적','2019_3Q_PL.csv'],
                    ['당기','2019_4Q_PL.csv'],
                    
                    ['당기 1분기 누적','2020_1Q_PL.csv'],
                    ['당기 반기 누적','2020_2Q_PL.csv'],
                    ['당기 3분기 누적','2020_3Q_PL.csv'],
                    ['당기','2020_4Q_PL.csv'],
                    
                    ['당기 1분기 누적','2021_1Q_PL.csv'],
                    ['당기 반기 누적','2021_2Q_PL.csv'],
                    ['당기 3분기 누적','2021_3Q_PL.csv'],
                    ['당기','2021_4Q_PL.csv']
                    ]
    for PL_info in PL_info_list:
        print("start :",PL_info[1])
        df=pd.read_csv("C:\\Users\\LG\\Desktop\\after_report_PL\\"+PL_info[1],encoding='cp949')

        df_PL = pd.read_csv("C:\\Users\\LG\\Desktop\\result_PL\\"+PL_info[1], encoding='cp949')
        def stock_code_preprocessing(df_data):
            stock_code = df_data['종목코드']
            stock_code = stock_code[1:-1]
            df_data['종목코드'] = stock_code
            return df_data

            
        # 가져온 데이터프레임에서 필요한 컬럼명만 추출
        df_txt = df.copy() # 불러온 df에 영향을 주지 않기 위해서 copy 사용
        df_txt = df_txt.apply(stock_code_preprocessing,axis=1) 

        df_PL=df_PL.set_index('종목코드')  
        
        check_null_frame = df_PL[df_PL['매출액'].isnull() | df_PL['영업이익'].isnull() | df_PL['당기순이익'].isnull() | df_PL['결산기준일'].isnull()].copy()
        display(check_null_frame) # 진행 전 결측치 출력
        
        if len(check_null_frame) >0:
            # 결측치를 매칭하는 함수 부분
            null_dict = dict() # 결측치들의 종목코드와 어떤 지표가 결측치인지 매칭 시키는 딕셔너리 생성
            def func2(df):
                if df.name not in null_dict:   
                    null_dict[df.name] = list(df[df.isnull()==True].index)
            check_null_frame.apply(func2)
            del null_dict['결산기준일'] # 결산기준일은 결측치가 없으므로 제거

        # csv파일에서 불러온 종목코드는 int 형이므로, str으로 변환, 나중에 계산을 편하게 하기 위해서
        temp_stock_list = list() # 여기에는 '당기순이익'이 결측치는 종목코드(str)들이 들어감
        for int_stock_code in null_dict['당기순이익']:
            str_stock_code = str(int_stock_code)
            zero_count = 6-len(str_stock_code)
            str_stock_code = '0'*zero_count + str_stock_code
            temp_stock_list.append(str_stock_code)
            
            
        
        for stock_code in temp_stock_list: # temp_stock_list에 있는 종목들에 대해서 진행
            ProfitLossBeforeTax = None # 법인세차감전이익
            # 데이터프레임이 존재하고, 원하는 컬럼의 값이 결측치가 아닌 실제 값일 경우에 값을 할당
            if (len(df_txt[(df_txt['종목코드'] == stock_code) & (df_txt['항목코드'] == 'ifrs_ProfitLossBeforeTax')])>0) and (list(df_txt[(df_txt['종목코드'] ==  stock_code) & (df_txt['항목코드'] == 'ifrs_ProfitLossBeforeTax')][PL_info[0]].values)[0] == list(df_txt[(df_txt['종목코드'] ==  stock_code) & (df_txt['항목코드'] == 'ifrs_ProfitLossBeforeTax')][PL_info[0]].values)[0]):
                ProfitLossBeforeTax = int(''.join(list(df_txt[(df_txt['종목코드'] == stock_code) & (df_txt['항목코드'] == 'ifrs_ProfitLossBeforeTax')][PL_info[0]].values)[0].split(',')))
                
            IncomeTaxExpenseContinuingOperations = None # 법인세
            if (len(df_txt[(df_txt['종목코드'] == stock_code) & (df_txt['항목코드'] == 'ifrs_IncomeTaxExpenseContinuingOperations')])>0) and (list(df_txt[(df_txt['종목코드'] ==  stock_code) & (df_txt['항목코드'] == 'ifrs_IncomeTaxExpenseContinuingOperations')][PL_info[0]].values)[0] == list(df_txt[(df_txt['종목코드'] ==  stock_code) & (df_txt['항목코드'] == 'ifrs_IncomeTaxExpenseContinuingOperations')][PL_info[0]].values)[0]):
                IncomeTaxExpenseContinuingOperations = int(''.join(list(df_txt[(df_txt['종목코드'] == stock_code) & (df_txt['항목코드'] == 'ifrs_IncomeTaxExpenseContinuingOperations')][PL_info[0]].values)[0].split(',')))
            
            if ProfitLossBeforeTax or ProfitLossBeforeTax ==0: # 법인세차감전이익이 0이 될수 도 있기에 고려
                if IncomeTaxExpenseContinuingOperations or IncomeTaxExpenseContinuingOperations ==0: # 법인세 0이 될수 도 있기에 고려
                    # print('법인세차감전순이익 :',ProfitLossBeforeTax)
                    # print('법인세 :',abs(IncomeTaxExpenseContinuingOperations))
                    # print("당기순이익 :",ProfitLossBeforeTax - abs(IncomeTaxExpenseContinuingOperations))
                    df_PL.loc[int(stock_code)]['당기순이익'] = ProfitLossBeforeTax - abs(IncomeTaxExpenseContinuingOperations)
                else: # 법인세가 결측치인 경우는 그냥 법인세 차감전 순이익을 순이익으로 계산
                    df_PL.loc[int(stock_code)]['당기순이익'] = ProfitLossBeforeTax
            
            # full만 붙음
            full_ProfitLossBeforeTax = None
            if (len(df_txt[(df_txt['종목코드'] == stock_code) & (df_txt['항목코드'] == 'ifrs-full_ProfitLossBeforeTax')])>0) and (list(df_txt[(df_txt['종목코드'] ==  stock_code) & (df_txt['항목코드'] == 'ifrs-full_ProfitLossBeforeTax')][PL_info[0]].values)[0] == list(df_txt[(df_txt['종목코드'] ==  stock_code) & (df_txt['항목코드'] == 'ifrs-full_ProfitLossBeforeTax')][PL_info[0]].values)[0]):
                full_ProfitLossBeforeTax = int(''.join(list(df_txt[(df_txt['종목코드'] == stock_code) & (df_txt['항목코드'] == 'ifrs-full_ProfitLossBeforeTax')][PL_info[0]].values)[0].split(',')))
                
            full_IncomeTaxExpenseContinuingOperations = None
            if (len(df_txt[(df_txt['종목코드'] == stock_code) & (df_txt['항목코드'] == 'ifrs-full_IncomeTaxExpenseContinuingOperations')])>0) and (list(df_txt[(df_txt['종목코드'] ==  stock_code) & (df_txt['항목코드'] == 'ifrs-full_IncomeTaxExpenseContinuingOperations')][PL_info[0]].values)[0] == list(df_txt[(df_txt['종목코드'] ==  stock_code) & (df_txt['항목코드'] == 'ifrs-full_IncomeTaxExpenseContinuingOperations')][PL_info[0]].values)[0]):
                full_IncomeTaxExpenseContinuingOperations = int(''.join(list(df_txt[(df_txt['종목코드'] == stock_code) & (df_txt['항목코드'] == 'ifrs-full_IncomeTaxExpenseContinuingOperations')][PL_info[0]].values)[0].split(',')))
            
            if full_ProfitLossBeforeTax or full_ProfitLossBeforeTax == 0:
                if full_IncomeTaxExpenseContinuingOperations or full_IncomeTaxExpenseContinuingOperations==0:
                    # print('법인세차감전순이익 :',full_ProfitLossBeforeTax)
                    # print('법인세 :',abs(full_IncomeTaxExpenseContinuingOperations))
                    # print("당기순이익 :",full_ProfitLossBeforeTax - abs(full_IncomeTaxExpenseContinuingOperations))
                    df_PL.loc[int(stock_code)]['당기순이익'] = full_ProfitLossBeforeTax - abs(full_IncomeTaxExpenseContinuingOperations)
                else:
                    df_PL.loc[int(stock_code)]['당기순이익'] = full_ProfitLossBeforeTax
            
            
        
        
        
        
        
        
        
        check_null_frame = df_PL[df_PL['매출액'].isnull() | df_PL['영업이익'].isnull() | df_PL['당기순이익'].isnull() | df_PL['결산기준일'].isnull()].copy()

        display(check_null_frame) # 진행 후 결측치 출력
        print()
        
        df_PL = df_PL.reset_index('종목코드') # 인덱스를 컬럼으로 초기화
        
        # 수정한 것 파일로 저장
        df_PL.to_csv('C:\\Users\\LG\\Desktop\\result_PL\\'+PL_info[1], index=False,encoding='cp949') # 파일로 저장

  # nan 인 값들이 따로 계산이 필요한 경우 직접 계산해서 대입
def modify_BS_file_2():
    BS_info_list = [
                    ['2017_3Q_BS.txt','당기 3분기말','2017_3Q_BS.csv'],
                    ['2017_4Q_BS.txt','당기','2017_4Q_BS.csv'],
                    
                    ['2018_1Q_BS.txt','당기 1분기말','2018_1Q_BS.csv'],
                    ['2018_2Q_BS.txt','당기 반기말','2018_2Q_BS.csv'],
                    ['2018_3Q_BS.txt','당기 3분기말','2018_3Q_BS.csv'],
                    
                    ['2020_4Q_BS.txt','당기','2020_4Q_BS.csv'],
                    
                    ['2021_1Q_BS.txt','당기 1분기말','2021_1Q_BS.csv'],
                    ['2021_2Q_BS.txt','당기 반기말','2021_2Q_BS.csv'],
                    ['2021_3Q_BS.txt','당기 3분기말','2021_3Q_BS.csv'],
                    ['2021_4Q_BS.txt','당기','2021_4Q_BS.csv']
                    ]
    for BS_info in BS_info_list:
    # 파일에 따라서 BS_info 수정

        print('start :',BS_info[2])
        df=pd.read_csv("C:\\Users\\LG\\Desktop\\report_BS\\"+BS_info[0],delimiter="\t", encoding='cp949')

        df_BS = pd.read_csv("C:\\Users\\LG\\Desktop\\result_BS\\"+BS_info[2], encoding='cp949')

        def stock_code_preprocessing(df_data):
            stock_code = df_data['종목코드']
            stock_code = stock_code[1:-1]
            df_data['종목코드'] = stock_code
            return df_data

            
        # 가져온 데이터프레임에서 필요한 컬럼명만 추출
        df_txt = df.copy() # 불러온 df에 영향을 주지 않기 위해서 copy 사용
        df_txt = df_txt.apply(stock_code_preprocessing,axis=1) 

        df_BS=df_BS.set_index('종목코드')
        
        # 2017_3Q_BS 일때
        if BS_info[2] == '2017_3Q_BS.csv':
            df_BS.loc[3720]['유동부채'] =107185653376

        
        # 2017_4Q_BS 일때
        if BS_info[2] == '2017_4Q_BS.csv':
            df_BS.loc[33500]['유동자산'] = 98574944426
            df_BS.loc[33500]['유동부채'] = 4285979386
        
        
        # 2018_1Q_BS 일때
        if BS_info[2] == '2018_1Q_BS.csv':
            df_BS.loc[89230]['유동자산'] = 37576200107
            df_BS.loc[89230]['유동부채'] = 8503250314
            
        
        # 2018_2Q_BS 일때
        if BS_info[2] == '2018_2Q_BS.csv':
            df_BS.loc[16740]['유동자산'] = 196005145601
            df_BS.loc[16740]['유동부채'] = 126374034537
            
            
        # 2018_3Q_BS 일때
        if BS_info[2] == '2018_3Q_BS.csv':
            df_BS.loc[16740]['유동자산'] = 181537768752
            df_BS.loc[16740]['유동부채'] = 111594039881


        # 2020_4Q_BS 일때
        if BS_info[2] == '2020_4Q_BS.csv':
            df_BS.loc[23460]['유동자산'] =271550775742
            df_BS.loc[23460]['유동부채'] =365733128000
        
        # 2021_1Q_BS 일때
        if BS_info[2] == '2021_1Q_BS.csv':
            df_BS.loc[23460]['유동자산'] = 331728860947
            df_BS.loc[23460]['유동부채'] = 402164602294
        

        # 2021_2Q_BS 일때
        if BS_info[2] == '2021_2Q_BS.csv':
            df_BS.loc[23460]['유동자산'] = 340446425943
            df_BS.loc[23460]['유동부채'] = 385559822745
            
        # 2021_3Q_BS 일때
        if BS_info[2] == '2021_3Q_BS.csv':
            df_BS.loc[23460]['유동자산'] = 273335570993
            df_BS.loc[23460]['유동부채'] = 381480631671
            
        # 2021_4Q_BS 일때
        if BS_info[2] == '2021_4Q_BS.csv':
            df_BS.loc[23460]['유동자산'] = 241685787747
            df_BS.loc[23460]['유동부채'] = 448576583855
            
        check_null_frame = df_BS[df_BS['유동자산'].isnull() | df_BS['자산총계'].isnull() | df_BS['유동부채'].isnull() | df_BS['부채총계'].isnull() | df_BS['결산기준일'].isnull()].copy()

        display(check_null_frame)
        
        df_BS = df_BS.reset_index('종목코드') # 인덱스를 컬럼으로 초기화
        
        # 수정한 것 파일로 저장
        df_BS.to_csv('C:\\Users\\LG\\Desktop\\result_BS\\'+BS_info[2], index=False,encoding='cp949') # 파일로 저장
        
# nan 인 값들이 따로 계산이 필요한 경우 직접 계산해서 대입
def modify_PL_file_2():
    PL_info_list = [
                    ['당기 1분기 누적','2016_1Q_PL.csv'],
                    ['당기 반기 누적','2016_2Q_PL.csv'],
                    ['당기 3분기 누적','2016_3Q_PL.csv'],
                    ['당기','2016_4Q_PL.csv'],
                    
                    ['당기 1분기 누적','2017_1Q_PL.csv'],
                    ['당기 반기 누적','2017_2Q_PL.csv'],
                    ['당기 3분기 누적','2017_3Q_PL.csv'],
                    ['당기','2017_4Q_PL.csv'],
                    
                    ['당기 1분기 누적','2018_1Q_PL.csv'],
                    ['당기 반기 누적','2018_2Q_PL.csv'],
                    ['당기 3분기 누적','2018_3Q_PL.csv'],
                    ['당기','2018_4Q_PL.csv'],
                    
                    ['당기 1분기 누적','2019_1Q_PL.csv'],
                    ['당기 반기 누적','2019_2Q_PL.csv'],
                    ['당기 3분기 누적','2019_3Q_PL.csv'],
                    ['당기','2019_4Q_PL.csv'],
                    
                    ['당기 1분기 누적','2020_1Q_PL.csv'],
                    ['당기 반기 누적','2020_2Q_PL.csv'],
                    ['당기 3분기 누적','2020_3Q_PL.csv'],
                    ['당기','2020_4Q_PL.csv'],
                    
                    ['당기 1분기 누적','2021_1Q_PL.csv'],
                    ['당기 반기 누적','2021_2Q_PL.csv'],
                    ['당기 3분기 누적','2021_3Q_PL.csv'],
                    ['당기','2021_4Q_PL.csv']
                    ]
    for PL_info in PL_info_list:
    # 파일에 따라서 BS_info 수정

        print('start :',PL_info[1])
        df=pd.read_csv("C:\\Users\\LG\\Desktop\\after_report_PL\\"+PL_info[1],encoding='cp949')

        df_PL = pd.read_csv("C:\\Users\\LG\\Desktop\\result_PL\\"+PL_info[1], encoding='cp949')

        def stock_code_preprocessing(df_data):
            stock_code = df_data['종목코드']
            stock_code = stock_code[1:-1]
            df_data['종목코드'] = stock_code
            return df_data

            
        # 가져온 데이터프레임에서 필요한 컬럼명만 추출
        df_txt = df.copy() # 불러온 df에 영향을 주지 않기 위해서 copy 사용
        df_txt = df_txt.apply(stock_code_preprocessing,axis=1) 

        df_PL=df_PL.set_index('종목코드')
        
        # 2016_1Q_BS 일때
        if PL_info[1] == '2016_1Q_PL.csv':
            df_PL.loc[35250]['매출액'] = 436574022144
            df_PL.loc[35250]['영업이익'] = 177874934338
            df_PL.loc[35250]['당기순이익'] = 142806287573
            
            df_PL.loc[151910]['매출액'] =12857454781	
            df_PL.loc[151910]['영업이익'] =-19041508028     
            
        elif PL_info[1] == '2017_1Q_PL.csv':   
            
            df_PL.loc[151910]['매출액'] = 8663237845
            df_PL.loc[151910]['영업이익'] = -261348057
            
        elif PL_info[1] == '2017_3Q_PL.csv':   
            df_PL.loc[39340]['매출액'] = 47912960563
            
        elif PL_info[1] == '2020_3Q_PL.csv':   
            df_PL.loc[39130]['당기순이익'] = -129621493549
            
            
        check_null_frame = df_PL[df_PL['매출액'].isnull() | df_PL['영업이익'].isnull() | df_PL['당기순이익'].isnull() | df_PL['결산기준일'].isnull()].copy()

        display(check_null_frame)
        
        df_PL = df_PL.reset_index('종목코드') # 인덱스를 컬럼으로 초기화
        df_PL.to_csv('C:\\Users\\LG\\Desktop\\result_PL\\'+PL_info[1], index=False,encoding='cp949') # 파일로 저장
        
        
# 매출액이 nan 인데 값이 0인 것들을 처리
def modify_PL_file_3():
    PL_info_list = [
                    
                    ['당기 1분기 누적','2019_1Q_PL.csv'],
                    ['당기 반기 누적','2019_2Q_PL.csv'],
                    ['당기 3분기 누적','2019_3Q_PL.csv'],
                    ['당기','2019_4Q_PL.csv'],
                    
                    ['당기 1분기 누적','2020_1Q_PL.csv'],
                    ['당기 반기 누적','2020_2Q_PL.csv'],
                    ['당기 3분기 누적','2020_3Q_PL.csv'],
                    ['당기','2020_4Q_PL.csv'],
                    
                    ['당기 1분기 누적','2021_1Q_PL.csv'],
                    ['당기 반기 누적','2021_2Q_PL.csv'],
                    ['당기 3분기 누적','2021_3Q_PL.csv'],
                    ['당기','2021_4Q_PL.csv']
                ]
    for PL_info in PL_info_list:
        print('start :',PL_info[1])
        df_PL = pd.read_csv("C:\\Users\\LG\\Desktop\\result_PL\\"+PL_info[1], encoding='cp949')
        df_PL=df_PL.set_index('종목코드')
        
        check_null_frame = df_PL[df_PL['매출액'].isnull() | df_PL['영업이익'].isnull() | df_PL['당기순이익'].isnull() | df_PL['결산기준일'].isnull()].copy()
        display(check_null_frame)
        
        if len(check_null_frame) >0:
            # 결측치를 매칭하는 함수 부분
            null_dict = dict() # 결측치들의 종목코드와 어떤 지표가 결측치인지 매칭 시키는 딕셔너리 생성
            def func2(df):
                if df.name not in null_dict:   
                    null_dict[df.name] = list(df[df.isnull()==True].index)
            check_null_frame.apply(func2)
            del null_dict['결산기준일'] # 결산기준일은 결측치가 없으므로 제거

        for stock_code in null_dict['매출액']:
            df_PL.loc[stock_code]['매출액'] = 0 # 매출액을 0으로 갱신
        check_null_frame = df_PL[df_PL['매출액'].isnull() | df_PL['영업이익'].isnull() | df_PL['당기순이익'].isnull() | df_PL['결산기준일'].isnull()].copy()
        display(check_null_frame)
        df_PL = df_PL.reset_index('종목코드') # 인덱스를 컬럼으로 초기화
        df_PL.to_csv('C:\\Users\\LG\\Desktop\\result_PL\\'+PL_info[1], index=False,encoding='cp949') # 파일로 저장
        

  

# make_BS_file()
# make_PL_file()

# modify_BS_file_1()
# modify_PL_file_1()

# modify_BS_file_2()
# modify_PL_file_2()
# modify_PL_file_3()