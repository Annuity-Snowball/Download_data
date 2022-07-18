# 포트폴리오 클래스 생성
class Portfolio():
    """
    포트폴리오 클래스 입니다
    __init__ 에서 포트폴리오 아이디를 데이터베이스에서 받는 부분은 구현 필요 합니다
    __init__ 에서 오류를 출력하는 부분(print(error))들은 예외 처리로 수정 필요합니다.
    __init__ 에서 입력받은 값들을 데이터베이스에 업데이트 하는 부분 구현이 필요합니다
    """
    
    # 파라미터들은 순서대로 str,int,str,str,int,str,int 형 들입니다
    def __init__(self,portfolio_name, strategy_count, start_time, end_time, rebalance_cycle, input_type, input_money):
        
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
        
        # 데이터베이스에 업데이트하는 부분
        pass # 추후 수정 필요
        
        
# 포트폴리오 생성 예씨
class_1=Portfolio('포트폴리오1',5,'20220101','20220501',12,'ML',20000)
print(class_1.__dict__)
        