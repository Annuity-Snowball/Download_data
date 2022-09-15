import pandas as pd

from IPython.display import display

def modify_BS_file():
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
        
        
        
        
def modify_PL_file():  
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
        
        
# modify_BS_file()
# modify_PL_file()