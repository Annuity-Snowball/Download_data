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
    
    # 메인함수에서 백테스트에 사용할 포트폴리오 객체 정보들을 넘겨주는 매소드
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
            start_time (str): 시작날짜
            end_time (str): 끝날짜
        """
        
        self.strategy_kind=strategy_kind
        self.product_count_per_strategy = product_count_per_strategy
        
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
    
# 포트폴리오 생성하기 위해서 내용을 입력받는 함수
def makePortfolio():
    portfolio_name = input("포트폴리오명은? : ")
    strategy_count = int(input("포트폴리오의 구성 전략 개수는? : "))
    start_time = input("백테스트 시작날짜(ex 20220101) : ")
    end_time = input("백테스트 끝날짜(ex 20220101) : ")
    rebalance_cycle = int(input("리밸런싱 주기(달 기준) : "))
    input_type = input("주기적으로 납입하는 방식 선택 : ")
    input_money = int(input("주기적으로 납입하는 금액 입력 : "))
    return portfolio_name, strategy_count, start_time, end_time, rebalance_cycle, input_type, input_money

def makeStrategy():
    strategy_kind = input("전략 종류를 입력하세요(ex PER 저, PBR 저) : ")
    product_count = int(input("전략의 구성 금융상품 개수를 입력하세요 : "))
    return strategy_kind, product_count
    
portfolio_name, strategy_count, start_time, end_time, rebalance_cycle, input_type, input_money=makePortfolio()

portfolio_1=Portfolio(portfolio_name, strategy_count, start_time, end_time, rebalance_cycle, input_type, input_money) # 포트폴리오면, 구성전략개수, 시작날짜, 끝날짜, 리밸런싱주기(달), 납입방법, 주기적납부금액

# 전략 생성 예시 - 사용자가 직접 입력할 수 있게 수정 필요
strategy_list = list()
for i in range(strategy_count):
    strategy_kind, product_count = makeStrategy()
    strategy_list.append(Strategy(strategy_kind, product_count))



print(portfolio_1.__dict__)
print(strategy_list)
for k in strategy_list:
    print(k.__dict__)

# 백테스트 함수 사용하기 위해서 리스트들 생성 -> 추후에 최적화 필요
# stratgy_kind_list = [strategy_1.getProductListQuery()[0],strategy_2.getProductListQuery()[0],strategy_3.getProductListQuery()[0]] # 전략종류(PER 저, PER 고 등)들을 받음
# stratgy_sql_query_list = [strategy_1.getProductListQuery()[1],strategy_2.getProductListQuery()[1],strategy_3.getProductListQuery()[1]] # 전략들에 따른 쿼리문들(날짜지정X)을 받음
