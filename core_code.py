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
    def getStratgyDate(self):
        return self.start_time,self.end_time
        
        
    # 전략에 해당하는 금융상품티커를 조회하는데 사용하는 쿼리문 반환하는 매소드
    def getProductList(self):
        """
        평가지표들에 따라서 쿼리문들을 추가해야 한다 -> 추가 및 수정필요!!
        """
        
        if self.strategy_kind == 'PER 저':
            # product_ticker, product_evaluate, estimated_per 명칭은 아직 미정 - 전략을 통해 선택할 금융상품개수까지 포함한 쿼리문
            sql_query='select product_ticker from product_evaluate order by estimated_per asc limit '+str(self.product_count_per_strategy)
        
        elif self.strategy_kind == 'PER 고':
            # product_ticker, product_evaluate, estimated_per 명칭은 아직 미정 - 전략을 통해 선택할 금융상품개수까지 포함한 쿼리문
            sql_query='select product_ticker from product_evaluate order by estimated_per desc limit '+str(self.product_count_per_strategy)
            
        # 위에서의 'PER 저', 'PER 고' 같이 모든 평가 지표들 마다 쿼리문을 작성할 것
        pass
        
        return sql_query

# 백테스트 함수 생성
def backTesting(portfolio_id, strategy_ratio, start_time, end_time, rebalance_cycle, input_type, input_money, product_ticker_query):
    """
    백테스트를 하는 함수
    백테스트를 직접하는 부분은 추가 구현 필요합니다!

    Args:
        portfolio_id (str): 포트폴리오 아이디
        strategy_ratio (list): 포트폴리오를 구성하는 전략별 비율, len()을 통해서 전략의 개수도 후에 구할 수 있음
        start_time (str): 조회 시작날짜
        end_time (str): 조회 끝날짜
        rebalance_cycle (int): 리밸런싱 주기
        input_type (str): 포트폴리오에서 금액 납입 방법
        input_money (int): 포트폴리오에서 납입 금액 액수
        product_ticker_query (str): Strategy에서 받아온 쿼리문
    """
    
    # 매달별 포트폴리오 계좌에 있는 금액을 표시하는 리스트 생성
    # portfolio_account = [
    #                         {'전략1':
    #                                 {
    #                                    '전략1로 선택한 금융상품1': [('날짜1','계좌에 있는 금융상품1을 통한 금액'),('날짜2','계좌에 있는 금융상품1을 통한 금액')],
    #                                    '전략1로 선택한 금융상품2': [('날짜1','계좌에 있는 금융상품2을 통한 금액'),('날짜2','계좌에 있는 금융상품2을 통한 금액')]
    #                                 }
    #                         },
    #                         {'전략2':
    #                                 {
    #                                     '전략2로 선택한 금융상품3': [('날짜1','계좌에 있는 금융상품3을 통한 금액'),('날짜2','계좌에 있는 금융상품3을 통한 금액')],
    #                                     '전략2로 선택한 금융상품4': [('날짜1','계좌에 있는 금융상품4을 통한 금액'),('날짜2','계좌에 있는 금융상품4을 통한 금액')]
    #                                 }
    #                         },
    #                         {'전략3':
    #                                 {
    #                                     '전략3로 선택한 금융상품5': [('날짜1','계좌에 있는 금융상품5을 통한 금액'),('날짜2','계좌에 있는 금융상품5을 통한 금액')],
    #                                     '전략3로 선택한 금융상품6': [('날짜1','계좌에 있는 금융상품6을 통한 금액'),('날짜2','계좌에 있는 금융상품6을 통한 금액')]
    #                                 }
    #                         },
    #                         {
    #                                 '포트폴리오 계좌추이':[('날짜1','계좌에 있는 포트폴리오 총 금액'),('날짜2','계좌에 있는 포트폴리오 총 금액')]
    #                         }
    #                     ]
    portfolio_account=list()
    
    
    
    
    

# 포트폴리오 생성 예시
portfolio_1=Portfolio('포트폴리오1',5,'20220101','20220501',12,'ML',20000)
strategy_1=Strategy('PER 저',3,'20220101','20220501')

# 생성한 객체 어트리뷰트들에 할당이 되었는지 확인
print(portfolio_1.__dict__)
print(strategy_1.__dict__)

# Strategy 클랙스로 생성한 객체를 통해 넘긴 쿼리문 확인
print(strategy_1.getProductList())
        