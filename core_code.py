from datetime import date, timedelta
import pymysql
import copy

from Download_data.getDatainfo import getDailyDateInfo, getPayInDateInfo, getRebalanceDateInfo, getYearlyDateInfo

from portpolioVariables import get_portVariables, get_returns,get_winRate, get_mdd, receipt_simul,cal_receiptValue 

# 포트폴리오 클래스 생성
class Portfolio():
    """
    포트폴리오 클래스 입니다
    추가적으로 백테스트 결과 반환하는 메소드들 개별로 추가해서 작성해야 합니다!
    """
    
    # 객체 생성할 때 초기화하는 매소드 입니다
    def __init__(self, portfolio_name, start_money, strategy_ratio, start_time, end_time, rebalance_cycle, input_type, input_money):
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
        
        
        # 포트폴리오 시작금액 입력받음
        self.start_money = start_money
        
        # 포트폴리오명 입력받음
        self.portfolio_name = portfolio_name
        
            
        # 구성 전략 개수 별 비율 입력 받기
        self.strategy_ratio= strategy_ratio
            
        # 포트폴리오 시작날짜, 끝날짜 입력받음(둘다 str 형태)
        self.start_time=start_time
        self.end_time=end_time
        
        # 리밸런싱 주기 입력받음
        self.rebalance_cycle = rebalance_cycle
        
        # 납입방법 입력 받음
        self.input_type = input_type
        
        # 주기적납입금액 입력받음
        self.input_money = input_money
        
        # 데이터베이스에 업데이트하는 부분 - sql 쿼리문
        pass # 추후 수정 필요
    
    # 메인함수에서 '백테스트'에 사용할 '포트폴리오 객체 정보'들을 넘겨주는 매소드
    def returnToBacktest(self):
        return self.portfolio_id, self.start_money, self.strategy_ratio, self.start_time, self.end_time, self.rebalance_cycle, self.input_type, self.input_money
              
# 전략 클래스 생성
class Strategy():
    """
    전략 클래스 입니다
    """
    
    # 객체 생성할 때 초기화하는 매소드 입니다
    def __init__(self,strategy_kind, product_count_per_strategy,min_value,max_value):
        """
        Args:
            strategy_kind (str): 전략종류(ex-'PER 저')를 입력 받음
            product_count_per_strategy (int): 한 전략에 해당하는 금융상품들 개수
        """
        
        self.strategy_kind=strategy_kind
        self.product_count_per_strategy = product_count_per_strategy
        if self.strategy_kind == 'PER':
            self.min_value = min_value
            self.max_value = max_value
        else:
            self.min_value = 0
            self.max_value = 0
        
    # 전략에 해당하는 금융상품티커를 조회하는데 사용하는 쿼리문  반환하는 매소드
    def getProductListQuery(self):
        """
        1. 평가지표(전략종류, 전략구성금융상품개수)들에 따라서 쿼리문들을 추가해야 한다 -> 추가 및 수정필요!!
        2. 평가지표
        날짜는 지정이 안되어 있는 쿼리문을 반환 합니다!
        """
        
        if self.strategy_kind == 'PER 저':
            # product_ticker, product_evaluate, estimated_per 명칭은 아직 미정 - 전략을 통해 선택할 금융상품개수까지 포함한 쿼리문
            self.sql_query='select product_date,product_ticker from product_evaluate order by per asc limit '+str(self.product_count_per_strategy)
        
        elif self.strategy_kind == 'PER 고':
            # product_ticker, product_evaluate, estimated_per 명칭은 아직 미정 - 전략을 통해 선택할 금융상품개수까지 포함한 쿼리문
            self.sql_query='select product_date,product_ticker from product_evaluate order by per desc limit '+str(self.product_count_per_strategy)
            
        # 평가지표의 범위를 입력받을 경우    
        elif self.strategy_kind == 'PER':
            # product_ticker, product_evaluate, estimated_per 명칭은 아직 미정 - 전략을 통해 선택할 금융상품개수까지 포함한 쿼리문
            self.sql_query='select product_date,product_ticker from product_evaluate where per >= '+str(self.min_value)+' and per <='+str(self.max_value)+' order by per asc limit '+str(self.product_count_per_strategy)
        
        elif self.strategy_kind == 'PBR 저':
            # product_ticker, product_evaluate, estimated_per 명칭은 아직 미정 - 전략을 통해 선택할 금융상품개수까지 포함한 쿼리문
            self.sql_query='select product_date,product_ticker from product_evaluate order by pbr asc limit '+str(self.product_count_per_strategy)
            
        elif self.strategy_kind == 'PBR 고':
        # product_ticker, product_evaluate, estimated_per 명칭은 아직 미정 - 전략을 통해 선택할 금융상품개수까지 포함한 쿼리문
            self.sql_query='select product_date,product_ticker from product_evaluate order by pbr desc limit '+str(self.product_count_per_strategy)
            
        # 위에서의 'PER 저', 'PER 고' 같이 모든 평가 지표들 마다 쿼리문을 작성할 것
        pass
        
        return self.strategy_kind, self.sql_query

# 백테스트 함수 생성
def backTesting(portfolio_id, start_rebalance_input_money, strategy_ratio, portfolio_start_time, 
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
        start_rebalance_input_money (int) : 초기시작 금액(시드머니), 시작금액이 없는 경우 0원으로 설정
        portfolio_id (str): 포트폴리오 아이디
        strategy_ratio (list): 포트폴리오를 구성하는 전략별 비율, len()을 통해서 전략의 개수도 후에 구할 수 있음
        start_time (str): 조회 시작날짜
        end_time (str): 조회 끝날짜
        rebalance_cycle (int): 리밸런싱 주기
        input_type (str): 포트폴리오에서 금액 납입 방법
        input_money (int): 포트폴리오에서 납입 금액 액수
        strategy_kinds (list): Strategy에서 받아온 전략들 종류들
        stratgy_sql_query_list (list): Strategy에서 받아온 쿼리문들
        tax(int) : 세제혜택 받을지 안받을지 여부, 1이면 세제혜택 받고, 0이면 세제혜택 받지 않음
    """
    
    # 시작날짜와 끝날짜 사이에 존채하는 모든 날짜들을 담은 리스트
    backtesting_date_list = getDailyDateInfo(portfolio_start_time, portfolio_end_time)
    
    # 리벨러스를 하는 날짜들 리스트(테스트용)
    rebalance_date_list = getRebalanceDateInfo(portfolio_start_time, portfolio_end_time, input_type, rebalance_cycle) # 리밸런싱 첫번째 날짜가 test_dates와 시작이 같아야 한다

    # 납입하는 날짜들을 담은 리스트(테스트용)
    input_date_list = getPayInDateInfo(portfolio_start_time, portfolio_end_time, input_type) # 납입한 날짜는 첫번째 날짜는 포함X
    
    # 세제혜택을 받는 날짜들을 남은 리스트
    tax_benfit_date_list = getYearlyDateInfo(portfolio_start_time, portfolio_end_time)
    
    
    # 납입하는 금액 히스토리
    input_money_count = 0 # 납입한 횟수(달별로 납입)
    input_money_to_portfolio=dict()
    for backtesting_date in backtesting_date_list:
        if backtesting_date in input_date_list[1:]:
            input_money_count+=1
        input_money_to_portfolio[backtesting_date] = input_money *input_money_count + start_rebalance_input_money
    
    
    
        
    # tax가 0이면 세제혜택 X, tax가 1이면 세제혜택 O
    for tax in range(2):
    
        tax_benefit_money = start_rebalance_input_money # 세제혜택을 받을 금액을 초기 금액으로 설정

        rebalanced_money_without_balance = start_rebalance_input_money

        total_balance_account= dict() # 날짜 별로 남은 잔액들 히스토리
        
        total_portfolio_account_without_balance = dict() # 날짜 별로 잔액을 제외한 포트폴리오 가치 히스토리
        
        current_balance_amount = 0 # 현재 잔액 총합 초기화
        
        recent_rebalance_date = None # 가장 최근 리밸런싱 한 날짜
        
        
        # a날짜 리밸런싱 -> a날 다음달 부터 a날 리밸런싱때 금융상품들로 주기적납부 -> b날 납부 -> b날 리밸런싱 ->  b날 다음달 부터 b날 리밸런싱때 금융상품들로 주기적납부
        # 백테스트기간 날짜들에 대해서 백테스트 진행!
        for backtesting_date in backtesting_date_list:
            
            # 세제혜택을 고려하고, 날짜가 세제환급받을 날짜들 중 하나이면
            if (backtesting_date in tax_benfit_date_list) and tax ==1:
                print('**********************************')
                print('세제혜택 받을 금액 :', tax_benefit_money)
                if tax_benefit_money >= 7000000: # 세제혜택 받을 금액이 700만원 이상이면(irp 기준)
                    tax_benefit_money = 7000000 * 0.165 # 700만원의 16.5% 금액을 환급
                else:# 세제혜택 받을 금액이 700만원 이하이면
                    tax_benefit_money *= 0.165 # 금액의 16.5% 금액을 환급
                # print('세제환급 받을 금액 :', tax_benefit_money)
                current_balance_amount += tax_benefit_money
                tax_benefit_money =0 # 세제혜택 받을 금액으로 0원으로 초기화
                print()
                
            # 조회날짜가 리밸런싱날짜에 있으면
            if backtesting_date in rebalance_date_list:
                # 리밸런싱을 하는 날이 납입날짜와 같을 경우
                # 처음 '리밸런싱하는 날'이 아닐 경우
                # '조회날짜'가 '납입날짜 리스트'에 있고, '조회날짜'가 '리밸런싱 날짜리스트'의 첫번째 날짜가 아니면(리밸런싱하는 첫번째 날이면 납입금액을 더하지 않아야 하므로)
                if backtesting_date in input_date_list and backtesting_date != rebalance_date_list[0]:
                    # '초기금액'에 '납입금액'을 더한다 -> '리밸런싱할 금액'을 구한다!
                    rebalanced_money_without_balance+=input_money
                    tax_benefit_money += input_money # 세제혜택을 받을 금액에 납입금액을 더함
                    
                recent_rebalance_date = backtesting_date # '최근 리밸런싱한 날짜'를 갱신
                print("==================================")
                print(recent_rebalance_date, "리밸런싱")
                print("==================================")
                # 리밸런싱 할 때 구매할 금융상품들 가격 구함
                portfolio_product_price = getPortfolioRebalanceProductPrice(stratgy_sql_query_list, strategy_kinds, recent_rebalance_date)
                print('리밸런싱 할 때 구매할 금융상품들 가격 :',portfolio_product_price)
                
                print('리밸런싱할 금액',rebalanced_money_without_balance+current_balance_amount) # 리밸런싱할 금액은 '포트폴리오가치(잔액X)'+'잔액' 이다
                
                rebalance_balance_account,portfolio_product_count = getPortfolioRabalanceInfo(portfolio_product_price,rebalanced_money_without_balance+current_balance_amount,strategy_ratio,recent_rebalance_date)
                print('리밸런싱 후 금융상품들 개수 :', portfolio_product_count)
                print("리밸런싱 후 잔액 :", rebalance_balance_account)
                
                portfolio_rebalance_product_value=getPortfolioProductValue(portfolio_product_price,portfolio_product_count)
                print('리밸런싱 후 금융상품들 가치 :',portfolio_rebalance_product_value)
                
                portfolio_rebalance_strategy_value=getPortfolioStrategyValue(portfolio_rebalance_product_value)
                print('리밸런싱 후 전략별 가치 :',portfolio_rebalance_strategy_value)
                
                portfolio_rebalance_value=getPortfolioValue(portfolio_rebalance_strategy_value)
                total_portfolio_account_without_balance[recent_rebalance_date]=portfolio_rebalance_value[recent_rebalance_date]
                print('리밸런싱 후 포트폴리오 가치(잔액포함X) :',total_portfolio_account_without_balance)
                
                total_balance_account[recent_rebalance_date] = rebalance_balance_account[recent_rebalance_date]
                print('리밸런싱 후 포트폴리오 잔액기록 :', total_balance_account)
                print()
                
                # 리밸런싱 할 때 마다 잔액 총합을 리밸런싱 하고 나서 나온 잔액을 잔액총합으로 설정
                current_balance_amount = total_balance_account[recent_rebalance_date]
            
            # 날씨가 납입날짜에 있으면
            elif backtesting_date in  input_date_list:
                print("==================================")
                print(backtesting_date, "납입날짜")
                print("==================================")
                portfolio_product_price=getPortfolioProductPrice(portfolio_product_price, backtesting_date)
                print('납부때마다 구매할 금융상품들 가격',portfolio_product_price)
                print('주기적 납부하는 돈 :', input_money)
                
                tax_benefit_money += input_money # 세졔혜택 받을 금액에 추가
                
                input_balance_account,new_portfolio_product_count=getPortfolioProductInfo(portfolio_product_price,input_money,strategy_ratio, backtesting_date)
                print('납부때마다 추가되는 금융상품 개수 :',new_portfolio_product_count)
                print('납부때마다 추가되는 잔액 :',input_balance_account)
                
                portfolio_product_count = getPortfolioProductAccumulateCount(portfolio_product_count,new_portfolio_product_count)
                print('누적 금융상품 개수 :',portfolio_product_count)
                
                portfolio_product_value=getPortfolioProductValue(portfolio_product_price,portfolio_product_count)
                print('누적 금융상품들 가치 :',portfolio_product_value)
                
                portfolio_strategy_value=getPortfolioStrategyValue(portfolio_product_value)
                print('누적 전략별 가치 :',portfolio_strategy_value)
                
                portfolio_rebalance_value=getPortfolioValue(portfolio_strategy_value)
                total_portfolio_account_without_balance[backtesting_date]=portfolio_rebalance_value[backtesting_date]
                # print('납입한 후 포트폴리오 가치(잔액포함X) :',total_portfolio_account_without_balance)
                
                # 포트폴리오 가치 총합을 갱신
                last_date = list(total_portfolio_account_without_balance.keys())[-1]
                rebalanced_money_without_balance = total_portfolio_account_without_balance[last_date]  # 잔액 제외 하고 리밸런싱할 금액을 갱신
                
                total_balance_account = getBalaceAccumulate(input_balance_account,total_balance_account) # 잔액 기록 갱신
                # print('누적 후 잔액기록 :',total_balance_account)
                
                current_balance_amount=total_balance_account[list(total_balance_account.keys())[-1]] # 현재 잔액현황 갱신
                print('납입한 후 리밸런싱 전까지 잔액 총합 :',current_balance_amount)
                print()
                
            else:
                print("==================================")
                print(backtesting_date, "나머지경우")
                print("==================================")
                portfolio_product_price=getPortfolioProductPrice(portfolio_product_price, backtesting_date)
                print(backtesting_date,'금융상품 가격 :',portfolio_product_price)
            
                portfolio_product_count=changeDateDictKey(portfolio_product_count,backtesting_date)
                print(backtesting_date,'금융상품 개수 :',portfolio_product_count)
                
                portfolio_product_value=getPortfolioProductValue(portfolio_product_price,portfolio_product_count)
                print(backtesting_date,'금융상품들 가치 :',portfolio_product_value)
                
                portfolio_strategy_value=getPortfolioStrategyValue(portfolio_product_value)
                print(backtesting_date,'전략별 가치 :',portfolio_strategy_value)
                
                portfolio_rebalance_value=getPortfolioValue(portfolio_strategy_value)
                total_portfolio_account_without_balance[backtesting_date]=portfolio_rebalance_value[backtesting_date]
                # print(backtesting_date,'포트폴리오 가치(잔액포함X) :',total_portfolio_account_without_balance)
                
                # 포트폴리오 가치 총합을 갱신
                last_date = list(total_portfolio_account_without_balance.keys())[-1]
                rebalanced_money_without_balance=total_portfolio_account_without_balance[last_date] # 잔액 제외 하고 리밸런싱할 금액을 갱신
                
                total_balance_account[backtesting_date] = current_balance_amount # 잔액기록에 현재잔액을 추가
                # print('누적 후 잔액기록 :',total_balance_account)
                print()
        
        print()
        if tax == 0: # 세제혜택 X 인 경우 결과값들 입력
            real_portfolio_account=getRealPortfolioValue(total_portfolio_account_without_balance,total_balance_account) # 포트폴리오 가치 추이
            portfolio_result = get_portVariables(real_portfolio_account,input_money_to_portfolio) # 포트폴리오 출력결과 변수
            portfolio_receipt = receipt_simul(portfolio_result,10) # 포트폴리오 수령방법, 몇년 수령할지 입력(10년 디폴트이고 나중에 사용자 맞게 수정 가능)

        elif tax == 1:# 세제혜택 0 인 경우 결과값들 입력
            real_portfolio_account_tax_benefit=getRealPortfolioValue(total_portfolio_account_without_balance,total_balance_account)
            portfolio_result_tax_benefit = get_portVariables(real_portfolio_account_tax_benefit,input_money_to_portfolio)
            portfolio_receipt_tax_benefit = receipt_simul(portfolio_result_tax_benefit,10) # 몇년 수령할지 입력(10년 디폴트이고 나중에 사용자 맞게 수정 가능)
    

    print("*************** 세제혜택X ***************")
    print()
    print('포트폴리오 가치 추이(잔액포함0):',real_portfolio_account)
    print()
    print('포트폴리오 납입금액 추이:', input_money_to_portfolio)
    print()
    print('포트폴리오 결과 :',portfolio_result)
    print()
    print('포트폴리오 수령방법 :',portfolio_receipt)
    
    print()
    print("*************** 세제혜택0 ***************")
    print()
    print('포트폴리오 가치 추이(잔액포함0):',real_portfolio_account_tax_benefit)
    print()
    print('포트폴리오 납입금액 추이:', input_money_to_portfolio)
    print()
    print('포트폴리오 결과 :', portfolio_result_tax_benefit)
    print()
    print('포트폴리오 수령방법 :',portfolio_receipt_tax_benefit)
 
# 날짜지정이 안되어 있는 쿼리문에서 날짜를 지정하는 부분을 추가해서 반환하는 함수 - 리밸런싱 날짜들을 받자!
def getProductTicker(sql_query,interval_dates):
    """
    
    Args:
    sql_query(str) : Strategy 클래스의 getProductListQuery() 매소드에서 받은 날짜지정이 안되어 있는 쿼리문
    interval_dates(list) : 납입날짜들 혹은 리밸런싱날짜들이 리스트로 입력받음
    
    Return:
    ex) product_ticker_infos = [
          [['2021-01-01', 'bank'], ['2021-01-01', 'energy'], ['2021-01-01', 'kospi']], 
          [['2021-02-01', 'bank'], ['2021-02-01', 'kospi'], ['2021-02-01', 'energy']], 
          [['2021-03-01', 'bank'], ['2021-03-01', 'kospi'], ['2021-03-01', 'energy']]
         ]
    """
    product_ticker_infos=list()
    
    # 입력받은 날짜들에 대해서 반복
    for interval_date in interval_dates:
    
        # Strategy 클래스의 getProductListQuery() 매소드에서 받은 날짜지정이 안되어 있는 쿼리문에 날짜 지정 부분을 추가
        get_product_ticker_query=sql_query.split(' ')
        if get_product_ticker_query[4] == 'where':
            get_product_ticker_query.insert(5,"product_date = '"+str(interval_date)+"' and")
        else:
            get_product_ticker_query.insert(4,"where product_date = '"+str(interval_date)+"'") 
        get_product_ticker_query=" ".join(get_product_ticker_query)

        # SQL 구문 실행하기 - sql 변수에 sql 명령어를 넣고 .execute()를 통해 실행
        snowball.execute(get_product_ticker_query) 
        
        # sql 결과값들로 조회한 값들을 anwers에 담음
        results=list(snowball.fetchall())
        
        # sql 데이터베이스에서 가져온 결과값들의 형변환
        for i in range(len(results)):
            results[i] = list(results[i]) # 기존 answers의 요소들의 tuple 형태가 수정 가능하게 list 타입으로 형 변환
            results[i][0] = str(results[i][0]) # 기존 answers의 요소의 첫번째 요소들이 date 타입이라 str 타입으로 형변환
            
        
        product_ticker_infos.append(results)
        
    # 데이터베이스에서 해당하는 날짜들, 금융상품티커 가져와서 반환 
    return product_ticker_infos

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

    # result는 데이터베이스에서 받아 온 결과물들을 담을 리스트
    result=snowball.fetchone()
    result=list(result)
    result.insert(0,product_ticker) # '금융상품티커'를 첫번째 인덱스에 추가
    
    # print('getProductPrice result :', result)
    return result
  
# 주기적으로 납입한 날의 새로 구매한 금융상품들 가격을 반환- 고정납입금액에 사용 
def getPortfolioProductPrice(portfolio_rebalance_product_price, test_date):
    product_price = copy.deepcopy(portfolio_rebalance_product_price)
    for strategy_kind_dict in product_price:
        for strategy_kind_key in strategy_kind_dict.keys():
            temp = strategy_kind_dict[strategy_kind_key] # temp 는 ex) {'2019-10-02': [['euro', 15963.0], ['spy', 12394.0]]}
            if len(list(temp.keys())) ==0: # 전략으로 인해 담을 금융상품이 없는 경우
                continue
            temp[test_date] = temp.pop(list(temp.keys())[0])
            for i,product_list in enumerate(temp[test_date]):
                temp[test_date][i] = getProductPrice(test_date,product_list[0])
    return product_price

# 주기적으로 납입한 날의 새로 구매한 금융상품들 개수을 반환 - 
def getPortfolioProductInfo(portfolio_product_price,input_money,strategy_ratio, test_date):
    """_summary_

    Args:
        portfolio_product_price (_type_): _description_
        input_money (_type_): _description_
        strategy_ratio (_type_): _description_

    Returns:
        _type_: ex)
    """
    
    # 복사를 통해서 portfolio_history 생성
    portfolio_product_count=copy.deepcopy(portfolio_product_price)
    
    input_balance_account=dict()
    input_balance_account[test_date] = 0
    input_money_ratio=list()

    for i in strategy_ratio:
        input_money_ratio.append(i*input_money//100)

    # print('input_money_ratio :',input_money_ratio)
    # print('before portfolio_product_count :', portfolio_product_count)
    # 전략별로 돌면서 실행
    for i,money in enumerate(input_money_ratio):
        product_price_dict = list(portfolio_product_count[i].values())[0]
        if len(list(product_price_dict)) <=0: # 전략에 해당하는 금융상품이 없을 때
            input_balance_account[test_date] += money # 할당 금액 전체가 잔액이 된다
            continue
        # print('product_price_dict :', product_price_dict) # {'2021-01-01': [['bank', 1269.0], ['energy', 4456.0], ['kospi', 22654.0]], '2021-02-01': [['bank', 1853.0], ['energy', 4145.0], ['kospi', 26166.0]], '2021-03-01': [['bank', 2048.0], ['energy', 3491.0], ['kospi', 14086.0]], '2021-04-01': [['bank', 2287.0], ['energy', 4060.0], ['kospi', 13185.0]]}
      
        # print('product_price_dict_keys :', product_price_dict_keys) #  ['2021-01-01', '2021-02-01', '2021-03-01', '2021-04-01']
        
            
        price_lists=product_price_dict[test_date] # [['bank', 2048.0], ['kospi', 14086.0], ['energy', 3491.0]] 
        # print('price_lists :',price_lists)
        money_to_price_list = money//len(price_lists)
        # print('money_to_price_list :',money_to_price_list)
        for price_list in price_lists:
            input_balance_account[test_date] += money_to_price_list % price_list[1]
            price_list[1] = int(money_to_price_list // price_list[1])
    
    # 일자별 잔액현황하고, 일자별 포트폴리오의 금융상품 개수들 반환
    return input_balance_account,portfolio_product_count

# 누적되는 금융상품개수 구하는 함수, 후자의 파라미터가 새로 구매한 금융상품 개수
def getPortfolioProductAccumulateCount(Portfolio_rebalance_product_count,Portfolio_product_count):
    
    portfolio_rebalance_product_count = copy.deepcopy(Portfolio_rebalance_product_count)
    portfolio_product_count = copy.deepcopy(Portfolio_product_count)
    
    for i in range(len(portfolio_product_count)):
        product_strategy_key=list(portfolio_product_count[i].keys())[0]
        product_strategy_value=portfolio_product_count[i][product_strategy_key]
        if len(list(product_strategy_value))<=0: # 전략에 해당하는 금융상품이 없는 경우
            continue # 차피 상품이 없을 것으므로 continu
        product_strategy_value_key=list(product_strategy_value.keys())[0] # strategy_value_keys 는 '2021-05-01' 등 날짜들
        
        rebalance_product_strategy_key=list(portfolio_rebalance_product_count[i].keys())[0]
        rebalance_product_strategy_value=portfolio_rebalance_product_count[i][rebalance_product_strategy_key]
        rebalance_product_strategy_value_key=list(rebalance_product_strategy_value.keys())[0]
        
        for i,product_list in enumerate(product_strategy_value[product_strategy_value_key]):
            product_list[1]+=rebalance_product_strategy_value[rebalance_product_strategy_value_key][i][1]
    return portfolio_product_count

# '리밸런싱 하는 날에 새로 구매할 금융상품들과 가격'을 반환
def getPortfolioRebalanceProductPrice(stratgy_sql_query_list,strategy_kinds,rebalance_date):
    """_summary_

    Args:
        sql_queries (_type_): 날짜를 제외한 '포트폴리오'를 구성하는 '전략종류'에 대응하는 값들을 가져오는 쿼리문!
        strategy_kinds (_type_): '포트폴리오'를 구성하는 '전략종류'들을 담은 리스트
        rebalance_date (_type_): '리밸런싱할 날짜'
    Returns:
        portfolio_rebalance_product_price : ex) [{'PER 저': {'2021-01-01': [['euro', 11315.0], ['china', 16981.0]]}}, {'PER 고': {'2021-01-01': [['qqq', 11679.0], ['spy', 11899.0], ['kospi', 13228.0]]}}, {'PBR 저': {'2021-01-01': [['bio', 16203.0], ['qqq', 11679.0], ['energy', 16678.0], ['spy', 11899.0]]}}]
    """
    
    portfolio_rebalance_product_price = list() # 반환할 '리밸런싱 할 때 구매할 금융상품들 가격' 리스트
    
    # '포트폴리오'를 구성하는 '전략종류' for 문이 돈다
    for i,sql_query in enumerate(stratgy_sql_query_list):
        # print()
        
        product_ticker_infos = getProductTicker(sql_query,[rebalance_date])
        # product_ticker_info 는 조회날짜 별로 전략에 따라 선택한 금융상품들의 티커의 정보를 담고 잇음
        # ex) product_ticker_infos = 
        # [
        #  [['2021-01-01', 'bank'], ['2021-01-01', 'energy'], ['2021-01-01', 'kospi']], 
        #  [['2021-02-01', 'bank'], ['2021-02-01', 'kospi'], ['2021-02-01', 'energy']], 
        #  [['2021-03-01', 'bank'], ['2021-03-01', 'kospi'], ['2021-03-01', 'energy']]
        # ]
        
        strategy_dict=dict() # key가 '전략명(전략종류)'등인 딕셔너리, '전략종류'가 바뀔 때마다 갱신을 해줘야 하므로 dict()로 초기화해주는 부분 필요
        
        product_dict=dict() # key가 '전략명(전략종류)'로 선택한 '금융상품'의 날짜' 인 딕셔러니
        
        # 3. 날짜에 대응하는 금융상품의 가격을 가져오는 부분 구현
        for product_ticker_info in product_ticker_infos:
            # print("product_ticker_info :",product_ticker_info)
            # ex) product_ticker_info = [['2021-01-01', 'bank'], ['2021-01-01', 'energy'], ['2021-01-01', 'kospi']]
            
            for product_date,product_ticker in product_ticker_info:
                # print('product_date, product_ticker :',product_date,product_ticker)
                
                # product_price_info 는 조회날짜 별로 전략에 따라 선택한 금융상품들의 가격의 정보를 담고 잇음
                product_price_info=getProductPrice(product_date,product_ticker)
                # print('product_price_info :',product_price_info)
                # ex) product_price_info = ['china', 5952.0]
                
                # key가 '전략명(전략종류)'로 선택한 '금융상품'의 날짜'인 딕셔러니 업데이트
                # key값이 product_date인 딕셔너리에 추가
                if product_date in product_dict:
                    product_dict[product_date].append(product_price_info)
                else: # 처음에는 key값이 product_date 인 딕셔너리가 없으니 생성을 해줘야 한다.
                    product_dict[product_date] = [product_price_info]
                    
        
        strategy_dict[strategy_kinds[i]]=product_dict #  key가 '전략명(전략종류)'등인 딕셔너리 업데이트
        
        
        # 이 부분을 통해서 for 문을 돌면서 '전략1','전략2' 등 전략들이 다 추가가 된다!
        portfolio_rebalance_product_price.append(strategy_dict)
    
    # 결과값을 반환!
    return portfolio_rebalance_product_price

# 리밸런싱 하는 날들에 새로 구매한 금융상품들과 그 개수를 반환, 잔액도 반환 - 리밸런싱에 사용
def getPortfolioRabalanceInfo(portfolio_rebalance_product_price,rebalance_input_money,strategy_ratio,test_date):
    
    portfolio_rebalance_product_count=copy.deepcopy(portfolio_rebalance_product_price)
    

    rebalance_balance_account=dict() # 일자별 잔액현황 선언
    rebalance_balance_account[test_date] =0 # 일자별 잔액현황 초기화
    input_money_ratio=list()
    for amount in strategy_ratio:
        input_money_ratio.append(amount*rebalance_input_money//100)

    # print('input_money_ratio :',input_money_ratio)
    # for i,input_money_ratio in enumerate(input_money_ratio_list): # input_money_ratio_list 는 [[400000, 600000], [800000, 1200000], [1200000, 1800000]] 
        #전략별로 반복
    for j,strategy_kind_money in enumerate(input_money_ratio): # input_money_ratio 는 ex) [400000, 600000], strategy_kind_money는 한 전략을 구입할 금액
        product_price_dict = list(portfolio_rebalance_product_count[j].values())[0]
        
        if len(product_price_dict) <= 0: # 해당 전략으로 살 상품이 없는경우
            rebalance_balance_account[test_date] +=strategy_kind_money # 할당된 금액 전체가 잔액이 된다
            continue
        price_lists=product_price_dict[test_date]
            
        # print('strategy_kind_money :', strategy_kind_money)
        # print('price_lists :', price_lists)
        strategy_product_money = int(strategy_kind_money // len(price_lists)) # strategy_product_money 는 전략에 해당하는 금융상품들중 한 금융상품을 구입할 금액
        # print('strategy_product_money :', strategy_product_money)
        # print('before balance_account : ',balance_account)
        for price_list in price_lists:
            # print('price_list[1] :',price_list[1])
            rebalance_balance_account[test_date] += strategy_product_money%price_list[1]
            # print('after balance_account : ',balance_account)
            price_list[1] = int(strategy_product_money//price_list[1])
                
            # print('after price_lists :', price_lists)
            # print()  
            
    # 일자별 잔액현황하고, 일자별 포트폴리오의 금융상품 개수들 반환
    return rebalance_balance_account, portfolio_rebalance_product_count

# 포트폴리오 내 새로 구매한 금융상품들 가치 반환
def getPortfolioProductValue(portfolio_rebalance_product_price,portfolio_rebalance_product_count):
    product_price = copy.deepcopy(portfolio_rebalance_product_price)
    product_count = copy.deepcopy(portfolio_rebalance_product_count)
    for i in range(len(product_price)):
        price_strategy_key=list(product_price[i].keys())[0]
        price_strategy_value=product_price[i][price_strategy_key]
        strategy_value_keys=list(price_strategy_value.keys())
        
        count_strategy_value=product_count[i][price_strategy_key]
        
        for strategy_value_key in strategy_value_keys:
            price_lists=price_strategy_value[strategy_value_key]
            count_lists=count_strategy_value[strategy_value_key]
            
            for i in range(len(price_lists)):
                price_lists[i][1] = price_lists[i][1] * count_lists[i][1]
    return(product_price)

# 포트폴리오 내 전략별 가치 반환
def getPortfolioStrategyValue(portfolio_rebalance_product_value):
    product_value = copy.deepcopy(portfolio_rebalance_product_value)
    for i in range(len(product_value)):
        price_strategy_key=list(product_value[i].keys())[0]
        price_strategy_value=product_value[i][price_strategy_key]
        strategy_value_keys=list(price_strategy_value.keys()) # strategy_value_keys 는 '2021-05-01' 등 날짜들
        
        
        for strategy_value_key in strategy_value_keys:
            sum=0
            price_lists=price_strategy_value[strategy_value_key]
            for price_list in price_lists:
                sum+=price_list[1]
            price_strategy_value[strategy_value_key] = sum
    return(product_value)

# 포트폴리오 내 가치반환(잔액포함X?)
def getPortfolioValue(portfolio_rebalance_strategy_value):
    portfolio_strategy_value = copy.deepcopy(portfolio_rebalance_strategy_value)
    portfolio_value=dict()

    # 전략별로 반복
    for i in range(len(portfolio_strategy_value)):
        price_strategy_key=list(portfolio_strategy_value[i].keys())[0]
        price_strategy_value=portfolio_strategy_value[i][price_strategy_key]
        strategy_value_keys=list(price_strategy_value.keys()) # strategy_value_keys 는 '2021-05-01' 등 날짜들
        
        
        for strategy_value_key in strategy_value_keys:
            if strategy_value_key in portfolio_value:
                portfolio_value[strategy_value_key]+=price_strategy_value[strategy_value_key]
            else:
                portfolio_value[strategy_value_key]=price_strategy_value[strategy_value_key]
    return(portfolio_value)

# 날짜 킷값 변경하는 함수
def changeDateDictKey(product_count,new_date):
    for i in range(len(product_count)):
        price_strategy_key=list(product_count[i].keys())[0]
        price_strategy_value=product_count[i][price_strategy_key]
        if len(list(price_strategy_value.keys())) <=0: # 전략에 해당하는 금융상품이 없는 경우
            continue
        price_strategy_value[new_date]=price_strategy_value.pop(list(price_strategy_value.keys())[0])
    return(product_count)

# 누적되는 잔액계좌 구하는 함수
def getBalaceAccumulate(input_balance_account,total_balance_account):
    new_balance_account_key = list(input_balance_account.keys())[0]

    total_balance_account[new_balance_account_key]=total_balance_account[list(total_balance_account.keys())[-1]]+list(input_balance_account.values())[0]
    
    return total_balance_account

# 포트폴리오 생성하기 위해서 내용을 입력받는 함수
def makePortfolio():
    portfolio_name = input("포트폴리오명은? : ")
    start_money = int(input("포트폴리오 시작금액은?(주기적 납입 금액 외의 시드 머니) : "))
    strategy_ratio = list(map(int,input("포트폴리오의 구성 전략 비율들는?(ex - 10 20 70 등으로 합쳐서 100이되게) : ").split()))
    start_time = input("백테스트 시작날짜(ex 2022-01-01) : ")
    end_time = input("백테스트 끝날짜(ex 2022-01-01) : ")
    rebalance_cycle = int(input("리밸런싱 주기(달 기준) : "))
    input_type = input("주기적으로 납입하는 방식 선택 : ")
    input_money = int(input("주기적으로 납입하는 금액 입력 : "))
    return portfolio_name,start_money, strategy_ratio, start_time, end_time, rebalance_cycle, input_type, input_money

def makeStrategy(strategy_count):
    stratgy_input_info_list = list() # 반환 할 리스트 생성
    for i in range(strategy_count): # 전략의 개수 만큼 입력을 받음
        temp_list = list()
        temp_list.append(input(str(i+1)+'번째 전략종류는? : '))
        temp_list.append(int(input(str(i+1)+'번째 전략으로 구매할 금융상품의 개수는? : ')))
        temp_list.append(int(input(str(i+1)+'번째 전략의 시작 수치는?(없으면 0) : ')))
        temp_list.append(int(input(str(i+1)+'번째 전략의 마지막 수치는?(없으면 0) : ')))
        stratgy_input_info_list.append(temp_list)
    return stratgy_input_info_list
   
# 잔액포함 포트폴리오 가치 반환하는 함수
def getRealPortfolioValue(total_portfolio_account,total_balance_account):
    real_portfolio_account = dict()

    for portfolio_key in total_portfolio_account.keys():
        real_portfolio_account[portfolio_key]=total_portfolio_account[portfolio_key]+total_balance_account[portfolio_key]
    return real_portfolio_account



 
# 실행하는 부분이 메인함수이면 실행 
if __name__ == "__main__":
    # 'makePortfoili() 함수' 를 이용해서 '포트폴리오 입력 변수'들을 생성
    portfolio_name, start_money, strategy_ratio, start_time, end_time, rebalance_cycle, input_type, input_money=makePortfolio()
    # '포트폴리오 입력 변수'와 'Portfolio() 클래스'를 이용해서 '포트폴리오 객체' 생성
    portfolio_1=Portfolio(portfolio_name, start_money, strategy_ratio, start_time, end_time, rebalance_cycle, input_type, input_money) # 포트폴리오면, 구성전략개수, 시작날짜, 끝날짜, 리밸런싱주기(달), 납입방법, 주기적납부금액
    
    
    strategy_list = list() # '포트폴리오'를 구성하는 '전략'들을 담을 '전략 리스트' 생성, '전략리스트' == '포트폴리오' 라고 생각해도 무관
    stratgy_input_info_list = makeStrategy(len(strategy_ratio)) # 전략생성을 위해서 기입할 정보드을 담을 리스트 ex) [['전략명1','전략으로담을금융상품개수1','수치입력일 경우 시작값', '수치입력을 경우 마지막값']]
                                                                # 백엔드 구현 시 함수 입력이 아닌 직접구현으로 교체
    for stratgy_input_info in stratgy_input_info_list: # '포트폴리오'를 구성하는 '전략의 개수'만큼 반복
        strategy_list.append(Strategy(*stratgy_input_info)) # 'Strategy() 클래스'를 이용해서 생성한 '전략'들을 '전략 리스트'에 추가
    
    # 접속하기 - 해당 데이터 베이스에 접속
    db = pymysql.connect(host='localhost', port=3306, user='root', passwd='yoy0317689*', db='snowball_database', charset='utf8') 
    snowball=db.cursor() 

    # 백테스트 함수 사용하기 위해서 리스트들 생성
    stratgy_kind_list = list() # '전략종류들을 담을 리스트' 생성 - '포트폴리오'를 구성하는 모든 '전략'들의 '전략종류'들이 담김
    stratgy_sql_query_list = list() # '전략종류를 통해 데이터베이스에서 정보를 가져올 쿼리문을 담을 리스트' 생성 - '포트폴리오'를 구성하는 모든 '전략'들의 '전략종류를 통해 데이터베이스에서 정보를 가져올 쿼리문'들이 담김
    
    for strategy_object in strategy_list: # '전략리스트' 에 있는 모든 '전략'들에 대해서 반복
        stratgy_kind_list.append(strategy_object.getProductListQuery()[0]) # '전략'의 '전략종류'을 '전략종류들을 담을 리스트'에 추가
        stratgy_sql_query_list.append(strategy_object.getProductListQuery()[1]) # '전략'의 '전략종류를 통해 데이터베이스에서 정보를 가져올 쿼리문'을 해당 리스트에 추가
    
    
    # 백테스트 함수 실행, 마지막 1은 세제혜택 여부에 따라 1 또는 0
    backTesting(*portfolio_1.returnToBacktest(), stratgy_kind_list, stratgy_sql_query_list)
    db.close()  