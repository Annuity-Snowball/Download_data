# 재무제표인 txt 파일들 csv 파일로 수정하여 저장하는 코드

import pandas as pd
from IPython.display import display
import csv

pdf_stock_list = list() # pdf에서 사용되는 종목코드들이 담겨 있는 리스트 생성
with open('C:\\self_project\\snowball\\Download_data\\need_stock_list.csv', newline='', encoding='utf-8') as csvfile:
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
                    category_name_list = ['매출액','영업수익','매출','영업수익(매출)','Ⅰ. 영업수익','매출과 지분법손익(영업수익)', 
                                          'Ⅰ.매출액','영업수익(매출과지분법손익)','I.매출액','수익','영업수익(매출액','영업수익(매출액)']
                elif null_category == 'OperatingIncomeLoss':
                    category_name_list = ['영업이익','영업이익(손실)','영업이익 (손실)', '영업손익', '영업 이익', 'Ⅲ. 영업이익', 'Ⅴ.영업이익', '영업손실','Ⅴ.영업이익(손실)','IV.영업이익(손실)']
                elif null_category == 'ProfitLoss':
                    category_name_list = ['당기순이익', '연결당기순이익', '당기연결순이익', '당기순이익(손실)', 'VI. 당기순이익(손실)', '당기순손익','Ⅷ.당기순이익(손실)']
                    
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
        display(check_null_frame)            
        df_PL.columns = ['매출액','영업이익','당기순이익','결산기준일'] # 컬럼명들을 수정
        df_PL = df_PL.reset_index('종목코드') # 인덱스를 컬럼으로 초기화
        df_PL.to_csv('C:\\Users\\LG\\Desktop\\result_PL\\'+PL_info[1], index=False,encoding='cp949') # 파일로 저장

    
    
# make_BS_file()
make_PL_file()