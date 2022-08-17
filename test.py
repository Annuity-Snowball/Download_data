from datetime import date, timedelta
import pymysql
import copy

from dateutil.parser import *
from dateutil.relativedelta import *
from dateutil.rrule import *
import exchange_calendars as ecal
import warnings
import time
import pandas as pd
from datetime import datetime

warnings.simplefilter(action='ignore', category=FutureWarning) # FutureWaring 제거

x = ecal.get_calendar("XKRX")

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
    
    # 메인함수에서 '백테스트'에 사용할 '포트폴리오 객체 정보'들을 넘겨주는 매소드
    def returnToBacktest(self):
        return self.portfolio_id, self.strategy_ratio, self.start_time, self.end_time, self.rebalance_cycle, self.input_type, self.input_money
              
# 전략 클래스 생성
class Strategy():
    """
    전략 클래스 입니다
    """
    
    # 객체 생성할 때 초기화하는 매소드 입니다
    def __init__(self,strategy_kind, product_count_per_strategy):
        """

        Args:
            strategy_kind (str): 전략종류(ex-'PER 저')를 입력 받음
            product_count_per_strategy (int): 한 전략에 해당하는 금융상품들 개수
        """
        
        self.strategy_kind=strategy_kind
        self.product_count_per_strategy = product_count_per_strategy
        
    # 전략의 시작날짜와 끝날짜를 반영하는 메소드
    # def getStratgyDate(self):
    #     return self.start_time,self.end_time
        
        
    # 전략에 해당하는 금융상품티커를 조회하는데 사용하는 쿼리문  반환하는 매소드
    def getProductListQuery(self):
        """
        평가지표(전략종류, 전략구성금융상품개수)들에 따라서 쿼리문들을 추가해야 한다 -> 추가 및 수정필요!!
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
                strategy_kinds, stratgy_sql_query_list):
    """
    백테스트를 하는 함수
    백테스트를 직접하는 부분은 추가 구현 필요합니다!
    1-1. 납입하는 날짜들을 계산하는 부분 구현 필요!
    1-2. 리밸런싱 하는 날짜들을 계산하는 부분 구현 필요
    테스트로 생성한, 납입날짜, 리밸런싱날짜들, 사이날짜들을 테스트용이 아닌 실제로 치환해야 한다
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
        stratgy_sql_query_list (list): Strategy에서 받아온 쿼리문들
    """
    
    
    
    
    
    # 1-2. 리밸런싱 하는 날짜들을 계산하는 부분 구현 필요 - test_start_rebalance_dates를 대체
    rebalance_date_list = list()
    
    
    
    
    # 처음 시작하는 금액 -> 초기금액이 없을 경우 0원으로 계산해야 함
    test_start_rebalance_input_money = 1000000
    


    getDailyDateInfo(portfolio_start_time, portfolio_end_time)
    # 시작날짜와 끝날짜 사이에 존채하는 모든 날짜들을 담은 리스트
    test_dates = getDailyDateInfo(portfolio_start_time, portfolio_end_time)
    print('테스트날짜들 :', test_dates)
    
    
    
    # 1-1. 납입하는 날짜들을 계산하는 부분 구현 필요 - test_input_date_lists를 대체
    input_date_list = getPayInDateInfo(portfolio_start_time, portfolio_end_time, 'first') # first, 
    print('input_date_list :', input_date_list)
    
    
    print('rebalance_date_list :',rebalance_date_list)
    
    
    

# 포트폴리오 생성하기 위해서 내용을 입력받는 함수
def makePortfolio():
    portfolio_name = input("포트폴리오명은? : ")
    strategy_count = int(input("포트폴리오의 구성 전략 개수는? : "))
    start_time = input("백테스트 시작날짜(ex 2022-01-01) : ")
    end_time = input("백테스트 끝날짜(ex 2022-01-01) : ")
    rebalance_cycle = int(input("리밸런싱 주기(달 기준) : "))
    input_type = input("주기적으로 납입하는 방식 선택 : ")
    input_money = int(input("주기적으로 납입하는 금액 입력 : "))
    return portfolio_name, strategy_count, start_time, end_time, rebalance_cycle, input_type, input_money
   
# 전략을 생성하기 위해서 내용을 입력받는 함수
def makeStrategy(i):
    strategy_kind = input(str(i+1)+"번째 전략 종류를 입력하세요(ex PER 저, PBR 저) : ")
    product_count = int(input("전략의 구성 금융상품 개수를 입력하세요 : "))
    return strategy_kind, product_count

# 시작날짜, 끝날짜 입력받은면 그 사이 개장일들을 반환해줌
def getDailyDateInfo(start_date, end_date):  # 지정한 기간 사이의 모든 개장일 반환
    a = x.sessions_in_range(start_date, end_date,)
    rtList = []

    for i in a:
        rtList.append(i.strftime('%Y-%m-%d'))

    return rtList

# 납입방법에 따라 날짜 계산해주는 함수(월초납입, 월말납입 중 하나 선택)
def getPayInDateInfo(start_date, end_date, interval):  # 납입일 계산 (월초 or 월말)
    rtList = []
    if interval == "first":
        a = list(rrule(MONTHLY, byweekday=(MO, TU, WE, TH, FR),
                       bysetpos=1,
                       dtstart=parse(start_date),
                       until=parse(end_date)))  # 지정된 기간의 매월 첫 평일 (월초)
        for i in a:
            if not x.is_session(i):  # 개장일이 아닌 날이 있는지 check
                i = x.next_open(i)  # 다음 개장일
            rtList.append(i.strftime('%Y-%m-%d'))  # yyyy-mm-dd 형식 변환
        return rtList  # 납입 예정일 리스트 출력

    else:
        a = list(rrule(MONTHLY,
                       byweekday=(MO, TU, WE, TH, FR),
                       bysetpos=-1,
                       dtstart=parse(start_date),
                       until=parse(end_date)))  # 지정된 기간의 매월 마지막 평일

        for i in a:
            if not x.is_session(i):  # 개장일이 아닌 날이 있는지 check
                i = x.previous_open(i)  # 직전 개장일
            rtList.append(i.strftime('%Y-%m-%d'))  # yyyy-mm-dd 형식 변환
        return rtList  # 납입 예정일 리스트 출력

    
# 실행하는 부분이 메인함수이면 실행 
if __name__ == "__main__":
    # 'makePortfoili() 함수' 를 이용해서 '포트폴리오 입력 변수'들을 생성
    portfolio_name, strategy_count, start_time, end_time, rebalance_cycle, input_type, input_money=makePortfolio()
    # '포트폴리오 입력 변수'와 'Portfolio() 클래스'를 이용해서 '포트폴리오 객체' 생성
    portfolio_1=Portfolio(portfolio_name, strategy_count, start_time, end_time, rebalance_cycle, input_type, input_money) # 포트폴리오면, 구성전략개수, 시작날짜, 끝날짜, 리밸런싱주기(달), 납입방법, 주기적납부금액
    
    
    strategy_list = list() # '포트폴리오'를 구성하는 '전략'들을 담을 '전략 리스트' 생성, '전략리스트' == '포트폴리오' 라고 생각해도 무관
    for i in range(strategy_count): # '포트폴리오'를 구성하는 '전략의 개수'만큼 반복
        strategy_kind, product_count = makeStrategy(i) # 'makeStrategy() 함수'를 이용해서 '전략종류(PER 저 등)'와 '전략으로 선택할 금융상품 개수'를 입력받음
        strategy_list.append(Strategy(strategy_kind, product_count)) # 'Strategy() 클래스'를 이용해서 생성한 '전략'들을 '전략 리스트'에 추가
    
    # 접속하기 - 해당 데이터 베이스에 접속
    db = pymysql.connect(host='localhost', port=3306, user='root', passwd='yoy0317689*', db='snowball_database', charset='utf8') 
    snowball=db.cursor() 

    # 백테스트 함수 사용하기 위해서 리스트들 생성
    stratgy_kind_list = list() # '전략종류들을 담을 리스트' 생성 - '포트폴리오'를 구성하는 모든 '전략'들의 '전략종류'들이 담김
    stratgy_sql_query_list = list() # '전략종류를 통해 데이터베이스에서 정보를 가져올 쿼리문을 담을 리스트' 생성 - '포트폴리오'를 구성하는 모든 '전략'들의 '전략종류를 통해 데이터베이스에서 정보를 가져올 쿼리문'들이 담김
    for strategy_object in strategy_list: # '전략리스트' 에 있는 모든 '전략'들에 대해서 반복
        stratgy_kind_list.append(strategy_object.getProductListQuery()[0]) # '전략'의 '전략종류'을 '전략종류들을 담을 리스트'에 추가
        stratgy_sql_query_list.append(strategy_object.getProductListQuery()[1]) # '전략'의 '전략종류를 통해 데이터베이스에서 정보를 가져올 쿼리문'을 해당 리스트에 추가
    
    
    # 백테스트 함수 실행
    backTesting(*portfolio_1.returnToBacktest(), stratgy_kind_list, stratgy_sql_query_list)
    db.close()  