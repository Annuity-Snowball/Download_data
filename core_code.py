from datetime import date, timedelta
import pymysql



# 포트폴리오 클래스 생성
class Portfolio():
    """
    포트폴리오 클래스 입니다
    추가적으로 백테스트 결과 반환하는 메소드들 개별로 추가해서 작성해야 합니다!
    """
    
    # 객체 생성할 때 초기화하는 매소드 입니다
    def __init__(self,portfolio_name, strategy_count, start_time, end_time, rebalance_cycle, input_type, input_money):
        """
        포트폴리오 아이디를 데이터베이스에서 받는 부분은 구현 필요 합니다
        오류를 출력하는 부분(print(error))들은 예외 처리로 수정 필요합니다.
        입력받은 값들을 데이터베이스에 업데이트 하는 부분 구현이 필요합니다
        
        Args:
            portfolio_name (str): 포트폴리오명
            strategy_count (int: 포트폴리오를 구성하는 전략의 개수
            start_time (str): 조회 시작날짜
            end_time (str): 조회 끝날짜
            rebalance_cycle (int): 리밸런싱하는 주기(달별로)
            input_type (str): MF,ML,YF,YL 식으로 매달,매초,연초,연말 등의 타입을 입력받을 수 있습니다
            input_money (int): 납입금액, 한번 납입할 때 얼마씩 납입하는 지 입력
        """
        
        # 포트폴리오아이디 생성
        self.portfolio_id='123456' # 추후 수정 필요
        
        # 포트폴리오명 입력받음
        self.portfolio_name = portfolio_name
        
        # 구성 전략 개수 입력받기
        if strategy_count<=5:
            self.strategy_count=strategy_count
        elif strategy_count>5: 
            print('error!') # 추후 수정 필요
            
        # 구성 전략 개수 별 비율 입력 받기
        self.strategy_ratio=list()
        for i in range(self.strategy_count):
            strategy_ratio=int(input('{}번째 전략은 포트폴리오의 몇 퍼센트? '.format(i+1)))
            self.strategy_ratio.append(strategy_ratio)
            
        if sum(self.strategy_ratio)!=100:
            print('error') # 추후 수정 필요
            
        # 포트폴리오 시작날짜, 끝날짜 입력받음(둘다 str 형태)
        self.start_time=start_time
        self.end_time=end_time
        
        # 리밸런싱 주기 입력받음
        self.rebalance_cycle = rebalance_cycle
        
        # 납입방법 입력 받음
        self.input_type = input_type
        
        # 납입금액 입력받음
        self.input_money = input_money
        
        # 데이터베이스에 업데이트하는 부분 - sql 쿼리문
        pass # 추후 수정 필요
    
    # 백테스트에 사용할 포트폴리오 객체 정보들을 넘겨주는 매소드
    def returnToBacktest(self):
        return self.portfolio_id, self.strategy_ratio, self.start_time, self.end_time, self.rebalance_cycle, self.input_type, self.input_money
              
# 전략 클래스 생성
class Strategy():
    """
    전략 클래스 입니다
    """
    
    # 객체 생성할 때 초기화하는 매소드 입니다
    def __init__(self,strategy_kind, product_count_per_strategy, start_time, end_time):
        """

        Args:
            strategy_kind (str): 전략종류(ex-'PER 저')를 입력 받음
            product_count_per_strategy (int): 한 전략에 해당하는 금융상품들 개수
            start_time (str): 시작날짜
            end_time (str): 끝날짜
        """
        
        self.strategy_kind=strategy_kind
        self.product_count_per_strategy = product_count_per_strategy
        self.start_time = start_time
        self.end_time = end_time
        
    # 전략의 시작날짜와 끝날짜를 반영하는 메소드
    # def getStratgyDate(self):
    #     return self.start_time,self.end_time
        
        
    # 전략에 해당하는 금융상품티커를 조회하는데 사용하는 쿼리문  반환하는 매소드
    def getProductListQuery(self):
        """
        평가지표들에 따라서 쿼리문들을 추가해야 한다 -> 추가 및 수정필요!!
        날짜는 지정이 안되어 있는 쿼리문을 반환 합니다!
        """
        
        if self.strategy_kind == 'PER 저':
            # product_ticker, product_evaluate, estimated_per 명칭은 아직 미정 - 전략을 통해 선택할 금융상품개수까지 포함한 쿼리문
            self.sql_query='select product_date,product_ticker from product_evaluate order by per asc limit '+str(self.product_count_per_strategy)
        
        elif self.strategy_kind == 'PER 고':
            # product_ticker, product_evaluate, estimated_per 명칭은 아직 미정 - 전략을 통해 선택할 금융상품개수까지 포함한 쿼리문
            self.sql_query='select product_date,product_ticker from product_evaluate order by per desc limit '+str(self.product_count_per_strategy)
        
        elif self.strategy_kind == 'PBR 저':
            # product_ticker, product_evaluate, estimated_per 명칭은 아직 미정 - 전략을 통해 선택할 금융상품개수까지 포함한 쿼리문
            self.sql_query='select product_date,product_ticker from product_evaluate order by pbr asc limit '+str(self.product_count_per_strategy)
            
        elif self.strategy_kind == 'PBR 고':
        # product_ticker, product_evaluate, estimated_per 명칭은 아직 미정 - 전략을 통해 선택할 금융상품개수까지 포함한 쿼리문
            self.sql_query='select product_date,product_ticker from product_evaluate order by pbr desc limit '+str(self.product_count_per_strategy)
            
        # 위에서의 'PER 저', 'PER 고' 같이 모든 평가 지표들 마다 쿼리문을 작성할 것
        pass
        
        return self.strategy_kind,self.sql_query

# 백테스트 함수 생성
def backTesting(portfolio_id, strategy_ratio, portfolio_start_time, 
                portfolio_end_time, rebalance_cycle, input_type, input_money, 
                strategy_kinds, sql_queries):
    """
    백테스트를 하는 함수
    백테스트를 직접하는 부분은 추가 구현 필요합니다!
    1-1. 납입하는 날짜들을 계산하는 부분 구현 필요!
    1-2. 리밸런싱 하는 날짜들을 계산하는 부분 구현 필요
    2. 전략으로 선택한 금융상품들을 가져오는 쿼리문 작성하는 부분 getProductTickerQuery()은 추가 수정 필요
    PortfolioInfo()를 통해서 PortfolioHistory() 와 PortfolioAccount() 도 만들어야 한다
    Args:
        portfolio_id (str): 포트폴리오 아이디
        strategy_ratio (list): 포트폴리오를 구성하는 전략별 비율, len()을 통해서 전략의 개수도 후에 구할 수 있음
        start_time (str): 조회 시작날짜
        end_time (str): 조회 끝날짜
        rebalance_cycle (int): 리밸런싱 주기
        input_type (str): 포트폴리오에서 금액 납입 방법
        input_money (int): 포트폴리오에서 납입 금액 액수
        strategy_kinds (list): Strategy에서 받아온 전략들 종류들
        sql_queries (list): Strategy에서 받아온 쿼리문들
    """
    
    
    
    # 1-1. 납입하는 날짜들을 계산하는 부분 구현 필요 - getDateInfo 이용
    input_date_list = list()
    
    # 1-2. 리밸런싱 하는 날짜들을 계산하는 부분 구현 필요 - getDateInfo 이용
    rebalance_date_list = list()
    
    # 2. 전략으로 선택한 금융상품들을 가져오는 쿼리문 작성하고 데이터베이스에서 받아오는 구현
    # poertfolio_info 는 포트폴리오에 있는 전략들의 조회당시 가격들이 담긴 리스트, portfolio_info_explain.py 참조
    portfolio_info = makePortfolioInfo(sql_queries, strategy_kinds)
    print(portfolio_info)
    pass
    
# 시작날짜, 끝날짜, 간격을 입력받으면 중간날짜들을 반환해주는 함수
def getDateInfo(start_date,end_date,interval):
    
    
    pass
 
# 해당날짜들에 대응하는 금융상품들 정보 반환하는 함수
def getProductTicker(sql_query,interval_dates):
    """
    
    1. str(20200101) 부분 수정 필요
    2. 데이터베이스에서 정보 가져오는 부분 구현 및 return 부분도 추가 필요
    
    Args:
    sql_query(str) : getProductListQuery() 에서 받은 날짜지정이 안되어 있는 쿼리문
    interval_dates(str) : 납입날짜들 혹은 리밸런싱날짜들이 리스트로 입력받음
    
    Return:
    ex) [['2021-01-01', 'bank'], ['2021-01-01', 'energy'], ['2021-01-01', 'kospi']]
    """
    result=list()
    for interval_date in interval_dates:
    
        # get_stratgy_price_query 는 전략종류에 따라서 가져온 금융상품의 정보(금융상품티커) 을 가져오는 쿼리
        get_product_ticker_query=sql_query.split(' ')
        get_product_ticker_query.insert(4,"where product_date = '"+str(interval_date)+"'") # str(20200101) 은 interval_dates들을 반복문으로 대입
        get_product_ticker_query=" ".join(get_product_ticker_query)

        # print('get_product_ticker_query :',get_product_ticker_query)
        
        # SQL 구문 실행하기 - sql 변수에 sql 명령어를 넣고 .execute()를 통해 실행
        snowball.execute(get_product_ticker_query) 
        
        # sql 결과값들로 조회한 값들을 anwers에 담음
        answers=list(snowball.fetchall())
        # print("before answers :",answers)
        for i in range(len(answers)):
            answers[i] = list(answers[i])
            answers[i][0] = str(answers[i][0])
        # print("after answers :",answers)
        result.append(answers)
        # print("result :",result)
    # 데이터베이스에서 해당하는 날짜들, 금융상품티커 가져와서 반환 
    # print('getProductTicker result :', result)
    return result

# 날짜에 대응하는 금융상품의 가격을 가져오는 함수
def getProductPrice(product_date,product_ticker):
    """
    1. 쿼리문 안에 있는 테이블 등 상세내용 수정 필요
    2. 쿼리문을 통해서 데이터베이스에 저장되어 있는 금융상품 가격 가져오는 부분 구현

    Args:
        product_dates (str): 금융상품 가격을 조회할 날짜들
        product_ticker (str): 조회할 금융상품의 티커
    Return:
        ex) ['china', 5952.0]
    """
    # 쿼리문 안에 있는 테이블 등 상세내용 수정 필요
    sql_query = "select high_price from price_"+product_ticker+" where product_date='"+product_date+"'"
    # print('getProductPrice query:',sql_query)

    # SQL 구문 실행하기 - sql 변수에 sql 명령어를 넣고 .execute()를 통해 실행
    snowball.execute(sql_query) 

    result=snowball.fetchone()
    result=list(result)
    result.insert(0,product_ticker)
    
    # print('getProductPrice result :', result)
    # 쿼리문을 통해서 데이터베이스에 저장되어 있는 금융상품 가격 가져오는 부분 구현 필요, return 부분도 수정 필요
    return result
  
# 포트폴리오 계좌 만드는 함수 - 
def makePortfolioInfo(sql_queries,strategy_kinds):
    """
    1. strategy_dict[strategy_kinds[i]+" 계좌금액"] 계산해서 금액들 추가하는 부분 구현 필요
    2. portfolio_info['포트폴리오 계좌금액']=[] 계산해서 금액들 추가하는 부분 구현 필요

    Args:
        portfolio_info (list): 포트폴리오계좌
        sql_queries (list): 쿼리문들이 담겨있는 리스트
        strategy_kinds (list): 전략 종류들이 담겨 있는 리스트

    """
    portfolio_info = list()
    
    # 전략 별로 for 문이 돈다
    for i,sql_query in enumerate(sql_queries):
        # print()
        # product_ticker_info 는 조회날짜 별로 전략에 따라 선택한 금융상품들의 티커의 정보를 담고 잇음
        # ex) product_ticker_infos = 
        # [
        #  [['2021-01-01', 'bank'], ['2021-01-01', 'energy'], ['2021-01-01', 'kospi']], 
        #  [['2021-02-01', 'bank'], ['2021-02-01', 'kospi'], ['2021-02-01', 'energy']], 
        #  [['2021-03-01', 'bank'], ['2021-03-01', 'kospi'], ['2021-03-01', 'energy']]
        # ]
        product_ticker_infos = getProductTicker(sql_query,['2021-01-01','2021-02-01','2021-03-01'])
        # print("product_ticker_infos: " ,product_ticker_infos)
        
        strategy_dict=dict() # key가 '전략1'등인 딕셔너리
        
        product_dict=dict() # key가 '전략1로 선택한 금융상품1 날짜' 등인 딕셔러니
        # 3. 날짜에 대응하는 금융상품의 가격을 가져오는 부분 구현 - for문 안에 함수 넣어서 구현!
        for product_ticker_info in product_ticker_infos:
            # print("product_ticker_info :",product_ticker_info)
            # ex) product_ticker_info = [['2021-01-01', 'bank'], ['2021-01-01', 'energy'], ['2021-01-01', 'kospi']]
            for product_date,product_ticker in product_ticker_info:
                
                # print('product_date, product_ticker :',product_date,product_ticker)
                # product_price_info 는 조회날짜 별로 전략에 따라 선택한 금융상품들의 가격의 정보를 담고 잇음
                # ex) product_price_info = ['china', 5952.0]
                product_price_info=getProductPrice(product_date,product_ticker)
                # print('product_price_info :',product_price_info)
                
                # key가 '전략1로 선택한 금융상품1' 등인 딕셔러니 추가
                if product_date in product_dict:
                    product_dict[product_date].append(product_price_info)
                else:
                    product_dict[product_date] = [product_price_info]
                    
        
        strategy_dict[strategy_kinds[i]]=product_dict # key가 '전략1'등인 딕셔너리 추가
        
        
        # 이 부분을 통해서 for 문을 돌면서 '전략1','전략2' 등 전략들이 다 추가가 된다!
        portfolio_info.append(strategy_dict)
    
    return portfolio_info

# 실행하는 부분이 메인함수이면 실행 
if __name__ == "__main__":
    # 포트폴리오 생성 예시
    portfolio_1=Portfolio('포트폴리오1',2,'20220101','20220501',12,'ML',20000)
    strategy_1=Strategy('PER 저',3,'20220101','20220501')
    strategy_2=Strategy('PER 고',2,'20220101','20220501')
    
    # 접속하기 - 해당 데이터 베이스에 접속
    db = pymysql.connect(host='localhost', port=3306, user='root', passwd='yoy0317689*', db='snowball_database', charset='utf8') 
    snowball=db.cursor() 


    # 백테스트 함수 사용하기 위해서 리스트들 생성 -> 추후에 최적화 필요
    stratgy_kind_list = [strategy_1.getProductListQuery()[0],strategy_2.getProductListQuery()[0]] # 전략종류(PER 저, PER 고 등)들을 받음
    stratgy_sql_query_list = [strategy_1.getProductListQuery()[1],strategy_2.getProductListQuery()[1]] # 전략들에 따른 쿼리문들(날짜지정X)을 받음
    
    # 백테스트 함수 실행
    backTesting(*portfolio_1.returnToBacktest(), stratgy_kind_list, stratgy_sql_query_list)
    db.close()  