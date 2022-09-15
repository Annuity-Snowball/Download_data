import pandas as pd

from IPython.display import display


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