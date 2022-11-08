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
    
    def get_portfolio_without_tax_benefit(self):
        pass

    def get_portfolio_with_tax_benefit(self):
        pass
    
              
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


# 임시로 전략 입력받기 위해서 생성, 추후에 삭제할 함수
def makeStrategy(strategy_count):
    stratgy_input_info_list = list() # 반환 할 리스트 생성
    for i in range(strategy_count): # 전략의 개수 만큼 입력을 받음
        temp_list = list()
        temp_list.append(input(str(i+1)+'번째 전략종류는? : '))
        temp_list.append(int(input(str(i+1)+'번째 전략으로 구매할 금융상품의 개수는? : ')))
        temp_list.append(int(input(str(i+1)+'번째 전략의 시작 수치는?(없으면 0) : ')))
        temp_list.append(int(input(str(i+1)+'번째 전략의 마지막 수치는?(없으면 0) : ')))
        stratgy_input_info_list.append(temp_list)
    print('나중에 이렇게 입력하는 걸로 대입 해야 합니다 :', stratgy_input_info_list) # [['PER 저', 2, 0, 0], ['PER 고', 3, 0, 0]]
    return stratgy_input_info_list

class backtest():
    def __init__(self,portfolio_id, portfolio_name, portfolio_start_money, strategy_ratio, portfolio_start_time, 
                portfolio_end_time, rebalance_cycle, input_type, input_money):
        
        self.portfolio_id = portfolio_id
        self.portfolio_name = portfolio_name
        self.portfolio_start_money = portfolio_start_money
        self.strategy_ratio = strategy_ratio
        self.portfolio_start_time = portfolio_start_time
        self.portfolio_end_time = portfolio_end_time
        self.rebalance_cycle = rebalance_cycle
        self.input_type = input_type
        self.input_money = input_money
        self.strategy_list = list()
        
        self.portfolio_object = Portfolio(self.portfolio_name, self.portfolio_start_money, self.strategy_ratio, self.portfolio_start_time, self.portfolio_end_time, self.rebalance_cycle, self.input_type, self.input_money)
        
        self.stratgy_input_info_list = makeStrategy(len(strategy_ratio)) # 전략생성을 위해서 기입할 정보드을 담을 리스트 ex) [['전략명1','전략으로담을금융상품개수1','수치입력일 경우 시작값', '수치입력을 경우 마지막값']]
                                                                # 백엔드 구현 시 함수 입력이 아닌 직접구현으로 교체
                                                                # 추후 이런식으로 직접 대입 [['PER 저', 2, 0, 0], ['PER 고', 3, 0, 0]]
                                                                
    
        for stratgy_input_info in self.stratgy_input_info_list: # '포트폴리오'를 구성하는 '전략의 개수'만큼 반복
            self.strategy_list.append(Strategy(*stratgy_input_info)) # 'Strategy() 클래스'를 이용해서 생성한 '전략'들을 '전략 리스트'에 추가
    


        # 백테스트 함수 사용하기 위해서 리스트들 생성
        self.stratgy_kind_list = list() # '전략종류들을 담을 리스트' 생성 - '포트폴리오'를 구성하는 모든 '전략'들의 '전략종류'들이 담김
        self.stratgy_sql_query_list = list() # '전략종류를 통해 데이터베이스에서 정보를 가져올 쿼리문을 담을 리스트' 생성 - '포트폴리오'를 구성하는 모든 '전략'들의 '전략종류를 통해 데이터베이스에서 정보를 가져올 쿼리문'들이 담김
        
        for strategy_object in self.strategy_list: # '전략리스트' 에 있는 모든 '전략'들에 대해서 반복
            self.stratgy_kind_list.append(strategy_object.getProductListQuery()[0]) # '전략'의 '전략종류명'들을 '전략종류들을 담을 리스트'에 추가 # ex ['PER 저', 'PER 고']
            self.stratgy_sql_query_list.append(strategy_object.getProductListQuery()[1]) # '전략'의 '전략종류를 통해 데이터베이스에서 정보를 가져올 쿼리문'들을 해당 리스트에 추가  ex) ['select product_date,product_ticker from product_evaluate order by per asc limit 2', 'select product_date,product_ticker from product_evaluate order by per desc limit 3']
            
            
        # 시작날짜와 끝날짜 사이에 존채하는 모든 날짜들을 담은 리스트
        self.backtesting_date_list = getDailyDateInfo(self.portfolio_start_time, self.portfolio_end_time)
        
        # 리벨러스를 하는 날짜들 리스트(테스트용)
        self.rebalance_date_list = getRebalanceDateInfo(self.portfolio_start_time, self.portfolio_end_time, self.input_type, self.rebalance_cycle) # 리밸런싱 첫번째 날짜가 test_dates와 시작이 같아야 한다

        # 납입하는 날짜들을 담은 리스트(테스트용)
        self.input_date_list = getPayInDateInfo(self.portfolio_start_time, self.portfolio_end_time, self.input_type) # 납입한 날짜는 첫번째 날짜는 포함X
        
        # 세제혜택을 받는 날짜들을 남은 리스트
        self.tax_benfit_date_list = getYearlyDateInfo(self.portfolio_start_time, self.portfolio_end_time)
        
        self.rebalance_date_list=['2017-10-10','2018-01-02','2018-04-02']
        self.input_date_list=['2017-11-01','2017-12-01','2018-01-02','2018-02-01','2018-03-02','2018-04-02']
        
        # 납입하는 금액 히스토리 - 나중에 do_backtest 안에 구현을 하고 이 부분은 제거 해야 할듯!
        input_money_count = 0 # 납입한 횟수(달별로 납입)
        self.input_money_to_portfolio=dict()
        for backtesting_date in self.backtesting_date_list:
            if backtesting_date in self.input_date_list[1:]:
                input_money_count+=1
            self.input_money_to_portfolio[backtesting_date] = self.input_money *input_money_count + self.portfolio_start_money
            
            
            
    # 날짜지정이 안되어 있는 쿼리문에서 날짜를 지정하는 부분을 추가해서 반환하는 함수 - 리밸런싱 날짜들을 받자!
    def getProductTicker(self, sql_query, interval_dates):

        product_ticker_infos=list()
        
        for interval_date in interval_dates:
        
            get_product_ticker_query=sql_query.split(' ')
            if get_product_ticker_query[4] == 'where':
                get_product_ticker_query.insert(5,"product_date = '"+str(interval_date)+"' and")
            else:
                get_product_ticker_query.insert(4,"where product_date = '"+str(interval_date)+"'") 
            get_product_ticker_query=" ".join(get_product_ticker_query)

            snowball.execute(get_product_ticker_query) 
            
            results=list(snowball.fetchall())
            
            for i in range(len(results)):
                results[i] = list(results[i]) 
                results[i][0] = str(results[i][0])
                
            product_ticker_infos.append(results)
            
        return product_ticker_infos
    
    
    # 날짜에 대응하는 금융상품의 가격을 가져오는 함수
    def getProductPrice(self, product_date, product_ticker):
        sql_query = "select high_price from price_"+product_ticker+" where product_date='"+product_date+"'"

        snowball.execute(sql_query) 

        result=snowball.fetchone()
        result=list(result)
        result.insert(0,product_ticker) 
        
        return result
      
      
    # '리밸런싱 하는 날에 새로 구매할 금융상품들과 가격'을 반환
    def getPortfolioToRebalanceProductPrice(self, stratgy_sql_query_list, strategy_list, rebalance_date):
        
        portfolio_rebalance_product_price = list() # 반환할 '리밸런싱 할 때 구매할 금융상품들 가격' 리스트
        
        for i,sql_query in enumerate(stratgy_sql_query_list):
            
            product_ticker_infos = self.getProductTicker(sql_query,[rebalance_date])

            strategy_dict=dict()
            
            product_dict=dict() 
            
            for product_ticker_info in product_ticker_infos:
                
                for product_date,product_ticker in product_ticker_info:
                    product_price_info= self.getProductPrice(product_date,product_ticker)
                    if product_date in product_dict:
                        product_dict[product_date].append(product_price_info)
                    else: 
                        product_dict[product_date] = [product_price_info]
                        
            
            strategy_dict[strategy_list[i]]=product_dict 
            
            
            portfolio_rebalance_product_price.append(strategy_dict)
        
        return portfolio_rebalance_product_price      
    
    
    # 리밸런싱 하는 날들에 새로 구매한 금융상품들과 그 개수를 반환, 잔액도 반환 - 리밸런싱에 사용
    def getPortfolioRabalanceInfo(self, portfolio_rebalance_product_price, rebalance_input_money, strategy_ratio, test_date):
        
        portfolio_rebalance_product_count=copy.deepcopy(portfolio_rebalance_product_price)
        

        rebalance_balance_account=dict()
        rebalance_balance_account[test_date] =0 
        input_money_ratio=list()
        for amount in strategy_ratio:
            input_money_ratio.append(amount*rebalance_input_money//100)

        for j,strategy_kind_money in enumerate(input_money_ratio):
            product_price_dict = list(portfolio_rebalance_product_count[j].values())[0]
            
            if len(product_price_dict) <= 0: 
                rebalance_balance_account[test_date] +=strategy_kind_money 
                continue
            price_lists=product_price_dict[test_date]
                
            strategy_product_money = int(strategy_kind_money // len(price_lists)) 
            for price_list in price_lists:
                rebalance_balance_account[test_date] += strategy_product_money%price_list[1]

                price_list[1] = int(strategy_product_money//price_list[1])

        return rebalance_balance_account, portfolio_rebalance_product_count
    
    # 포트폴리오 내 새로 구매한 금융상품들 가치 반환
    def getPortfolioProductValue(self, portfolio_rebalance_product_price, portfolio_rebalance_product_count):
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
    def getPortfolioStrategyValue(self,portfolio_rebalance_product_value):
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
    def getPortfolioValueWithoutBalance(self,portfolio_rebalance_strategy_value):
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
            
            
    # 주기적으로 납입한 날의 새로 구매한 금융상품들 가격을 반환- 고정납입금액에 사용 
    def getPortfolioProductPrice(self,portfolio_rebalance_product_price, test_date):
        product_price = copy.deepcopy(portfolio_rebalance_product_price)
        for strategy_kind_dict in product_price:
            for strategy_kind_key in strategy_kind_dict.keys():
                temp = strategy_kind_dict[strategy_kind_key] # temp 는 ex) {'2019-10-02': [['euro', 15963.0], ['spy', 12394.0]]}
                if len(list(temp.keys())) ==0: # 전략으로 인해 담을 금융상품이 없는 경우
                    continue
                temp[test_date] = temp.pop(list(temp.keys())[0])
                for i,product_list in enumerate(temp[test_date]):
                    temp[test_date][i] = self.getProductPrice(test_date,product_list[0])
        return product_price  
    
     # 주기적으로 납입한 날의 새로 구매한 금융상품들 개수을 반환 - 
    def getPortfolioProductInfo(self,portfolio_product_price,input_money,strategy_ratio, test_date):
        
        # 복사를 통해서 portfolio_history 생성
        portfolio_product_count=copy.deepcopy(portfolio_product_price)
        
        input_balance_account=dict()
        input_balance_account[test_date] = 0
        input_money_ratio=list()

        for i in strategy_ratio:
            input_money_ratio.append(i*input_money//100)

        for i,money in enumerate(input_money_ratio):
            product_price_dict = list(portfolio_product_count[i].values())[0]
            if len(list(product_price_dict)) <=0: 
                input_balance_account[test_date] += money 
            price_lists=product_price_dict[test_date] # [['bank', 2048.0], ['kospi', 14086.0], ['energy', 3491.0]] 

            money_to_price_list = money//len(price_lists)
    
            for price_list in price_lists:
                input_balance_account[test_date] += money_to_price_list % price_list[1]
                price_list[1] = int(money_to_price_list // price_list[1])
     
        return input_balance_account,portfolio_product_count


    # 누적되는 금융상품개수 구하는 함수, 후자의 파라미터가 새로 구매한 금융상품 개수
    def getPortfolioProductAccumulateCount(self,Portfolio_rebalance_product_count,Portfolio_product_count):
        
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

    # 잔액포함 포트폴리오 가치 반환하는 함수
    def getRealPortfolioValue(self,total_portfolio_account,total_balance_account):
        real_portfolio_account = dict()

        for portfolio_key in total_portfolio_account.keys():
            real_portfolio_account[portfolio_key]=total_portfolio_account[portfolio_key]+total_balance_account[portfolio_key]
        return real_portfolio_account
    
    def updateToRecentDate(self,portfolio_product_count_account,new_date):
        for i in range(len(portfolio_product_count_account)):
            price_strategy_key=list(portfolio_product_count_account[i].keys())[0]
            price_strategy_value=portfolio_product_count_account[i][price_strategy_key]
            if len(list(price_strategy_value.keys())) <=0: # 전략에 해당하는 금융상품이 없는 경우
                continue
            price_strategy_value[new_date]=price_strategy_value.pop(list(price_strategy_value.keys())[0])
        return(portfolio_product_count_account)
          
    def do_backtest(self):

        # tax가 0이면 세제혜택 X, tax가 1이면 세제혜택 O
        for tax in range(2):
        
            tax_benefit_money = self.portfolio_start_money # 세제혜택을 받을 금액을 초기 금액으로 설정

            rebalanced_money_without_balance = self.portfolio_start_money

            total_balance_account= dict() # 날짜 별로 남은 잔액들 히스토리
            
            total_portfolio_without_balance_account = dict() # 날짜 별로 잔액을 제외한 포트폴리오 가치 히스토리
            
            current_balance_amount = 0 # 현재 잔액 총합 초기화
            
            recent_rebalance_date = None # 가장 최근 리밸런싱 한 날짜
            
            self.portfolio_balance_account = dict() 
            self.portfolio_product_count_account = None
            
            
            # a날짜 리밸런싱 -> a날 다음달 부터 a날 리밸런싱때 금융상품들로 주기적납부 -> b날 납부 -> b날 리밸런싱 ->  b날 다음달 부터 b날 리밸런싱때 금융상품들로 주기적납부
            # 백테스트기간 날짜들에 대해서 백테스트 진행!
            for backtesting_date in self.backtesting_date_list:
                
                # 세제혜택을 고려하고, 날짜가 세제환급받을 날짜들 중 하나이면
                if (backtesting_date in self.tax_benfit_date_list) and tax ==1:
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
                if backtesting_date in self.rebalance_date_list:
                    # 리밸런싱을 하는 날이 납입날짜와 같을 경우
                    # 처음 '리밸런싱하는 날'이 아닐 경우
                    # '조회날짜'가 '납입날짜 리스트'에 있고, '조회날짜'가 '리밸런싱 날짜리스트'의 첫번째 날짜가 아니면(리밸런싱하는 첫번째 날이면 납입금액을 더하지 않아야 하므로)
                    if backtesting_date in self.input_date_list and backtesting_date != self.rebalance_date_list[0]:
                        # '초기금액'에 '납입금액'을 더한다 -> '리밸런싱할 금액'을 구한다!
                        rebalanced_money_without_balance+=self.input_money
                        tax_benefit_money += self.input_money # 세제혜택을 받을 금액에 납입금액을 더함
                        
                    recent_rebalance_date = backtesting_date # '최근 리밸런싱한 날짜'를 갱신
                    print("==================================")
                    print(recent_rebalance_date, "리밸런싱")
                    print("==================================")
                    # 리밸런싱 할 때 구매할 금융상품들 가격 구함
                    portfolio_product_price = self.getPortfolioToRebalanceProductPrice(self.stratgy_sql_query_list, self.stratgy_kind_list, recent_rebalance_date)
                    print('리밸런싱 할 때 구매할 금융상품들 가격 :',portfolio_product_price)
                    
                    print('리밸런싱할 금액',rebalanced_money_without_balance+current_balance_amount) # 리밸런싱할 금액은 '포트폴리오가치(잔액X)'+'잔액' 이다
                    
                    rebalance_balance_account, self.portfolio_product_count_account = self.getPortfolioRabalanceInfo(portfolio_product_price,rebalanced_money_without_balance+current_balance_amount, self.strategy_ratio, recent_rebalance_date)
                    print('리밸런싱 후 금융상품들 개수 :', self.portfolio_product_count_account)
                    print("리밸런싱 후 잔액 :", rebalance_balance_account)
                    
                    portfolio_rebalance_product_value= self.getPortfolioProductValue(portfolio_product_price, self.portfolio_product_count_account)
                    print('리밸런싱 후 금융상품들 가치 :',portfolio_rebalance_product_value)
                    
                    portfolio_rebalance_strategy_value=self.getPortfolioStrategyValue(portfolio_rebalance_product_value)
                    print('리밸런싱 후 전략별 가치 :',portfolio_rebalance_strategy_value)
                    
                    portfolio_rebalance_value_without_balance=self.getPortfolioValueWithoutBalance(portfolio_rebalance_strategy_value)
                    total_portfolio_without_balance_account[recent_rebalance_date]=portfolio_rebalance_value_without_balance[recent_rebalance_date]
                    print('리밸런싱 후 포트폴리오 가치(잔액포함X) :',total_portfolio_without_balance_account)
                    
                    self.portfolio_balance_account[recent_rebalance_date] = rebalance_balance_account[recent_rebalance_date]
                    print('리밸런싱 후 포트폴리오 잔액기록 :', self.portfolio_balance_account)
                    print()
                    
                    # 리밸런싱 할 때 마다 잔액 총합을 리밸런싱 하고 나서 나온 잔액을 잔액총합으로 설정
                    current_balance_amount =self.portfolio_balance_account[recent_rebalance_date]
                
                # 날씨가 납입날짜에 있으면
                elif backtesting_date in self.input_date_list:
                    print("==================================")
                    print(backtesting_date, "납입날짜")
                    print("==================================")
                    portfolio_product_price=self.getPortfolioProductPrice(portfolio_product_price, backtesting_date)
                    print('납부때마다 구매할 금융상품들 가격',portfolio_product_price)
                    print('주기적 납부하는 돈 :', self.input_money)
                    
                    self.tax_benefit_money += self.input_money # 세졔혜택 받을 금액에 추가
                    
                    input_balance_account,new_portfolio_product_count=self.getPortfolioProductInfo(portfolio_product_price, self.input_money, self.strategy_ratio, backtesting_date)
                    print('납부때마다 추가되는 금융상품 개수 :',new_portfolio_product_count)
                    print('납부때마다 추가되는 잔액 :',input_balance_account)
                    
                    self.portfolio_product_count_account = self.getPortfolioProductAccumulateCount(self.portfolio_product_count_account, new_portfolio_product_count)
                    print('누적 금융상품 개수 :', self.portfolio_product_count_account)
                    
                    portfolio_product_value=self.getPortfolioProductValue(portfolio_product_price, self.portfolio_product_count_account)
                    print('누적 금융상품들 가치 :',portfolio_product_value)
                    
                    portfolio_strategy_value=self.getPortfolioStrategyValue(portfolio_product_value)
                    print('누적 전략별 가치 :',portfolio_strategy_value)
                    
                    portfolio_rebalance_value = self.getPortfolioValueWithoutBalance(portfolio_strategy_value)
                    total_portfolio_without_balance_account[backtesting_date]=portfolio_rebalance_value[backtesting_date]
                    # print('납입한 후 포트폴리오 가치(잔액포함X) :',  total_portfolio_without_balance_account)
                    
                    # 포트폴리오 가치 총합을 갱신
                    rebalanced_money_without_balance = total_portfolio_without_balance_account[backtesting_date]  # 잔액 제외 하고 리밸런싱할 금액을 갱신
                    
                    
                    self.portfolio_balance_account[backtesting_date] = self.portfolio_balance_account[self.portfolio_balance_account.keys()[-1]]+input_balance_account[backtesting_date]
                    
                    
                    current_balance_amount = self.portfolio_balance_account[self.portfolio_balance_account.keys()[-1]]
                    print('납입한 후 리밸런싱 전까지 잔액 총합 :',current_balance_amount)
                    print()
                    
                else:
                    print("==================================")
                    print(backtesting_date, "나머지경우")
                    print("==================================")
                    portfolio_product_price=self.getPortfolioProductPrice(portfolio_product_price, backtesting_date)
                    print(backtesting_date,'금융상품 가격 :',portfolio_product_price)
                
                    self.portfolio_product_count_account=self.updateToRecentDate(self.portfolio_product_count_account,backtesting_date)
                    print(backtesting_date,'금융상품 개수 :',self.portfolio_product_count_account)
                    
                    portfolio_product_value = self.getPortfolioProductValue(portfolio_product_price, self.portfolio_product_count_account)
                    print(backtesting_date,'금융상품들 가치 :',portfolio_product_value)
                    
                    portfolio_strategy_value = self.getPortfolioStrategyValue(portfolio_product_value)
                    print(backtesting_date,'전략별 가치 :',portfolio_strategy_value)
                    
                    portfolio_rebalance_value= self.getPortfolioValueWithoutBalance(portfolio_strategy_value)
                    total_portfolio_without_balance_account[backtesting_date]=portfolio_rebalance_value[backtesting_date]
                    # print(backtesting_date,'포트폴리오 가치(잔액포함X) :',total_portfolio_without_balance_account)
                    
                    # 포트폴리오 가치 총합을 갱신
                    rebalanced_money_without_balance = total_portfolio_without_balance_account[backtesting_date]
                    
                    self.portfolio_balance_account[backtesting_date] = self.portfolio_balance_account[self.portfolio_balance_account.keys()[-1]]
                    # print('누적 후 잔액기록 :',total_balance_account)
                    print()
            
            print()
            if tax == 0: # 세제혜택 X 인 경우 결과값들 입력
                real_portfolio_account=self.getRealPortfolioValue(total_portfolio_without_balance_account,total_balance_account) # 포트폴리오 가치 추이
                portfolio_result = get_portVariables(real_portfolio_account, self.input_money_to_portfolio) # 포트폴리오 출력결과 변수
                portfolio_receipt = receipt_simul(portfolio_result,10) # 포트폴리오 수령방법, 몇년 수령할지 입력(10년 디폴트이고 나중에 사용자 맞게 수정 가능)

            elif tax == 1:# 세제혜택 0 인 경우 결과값들 입력
                real_portfolio_account_tax_benefit=self.getRealPortfolioValue(total_portfolio_without_balance_account,total_balance_account)
                portfolio_result_tax_benefit = get_portVariables(real_portfolio_account_tax_benefit, self.input_money_to_portfolio)
                portfolio_receipt_tax_benefit = receipt_simul(portfolio_result_tax_benefit,10) # 몇년 수령할지 입력(10년 디폴트이고 나중에 사용자 맞게 수정 가능)
        

        print("*************** 세제혜택X ***************")
        print()
        print('포트폴리오 가치 추이(잔액포함0):',real_portfolio_account)
        print()
        print('포트폴리오 납입금액 추이:', self.input_money_to_portfolio)
        print()
        print('포트폴리오 결과 :',portfolio_result)
        print()
        print('포트폴리오 수령방법 :',portfolio_receipt)
        
        print()
        print("*************** 세제혜택0 ***************")
        print()
        print('포트폴리오 가치 추이(잔액포함0):',real_portfolio_account_tax_benefit)
        print()
        print('포트폴리오 납입금액 추이:', self.input_money_to_portfolio)
        print()
        print('포트폴리오 결과 :', portfolio_result_tax_benefit)
        print()
        print('포트폴리오 수령방법 :',portfolio_receipt_tax_benefit)
    
    
    
    

 
# 실행하는 부분이 메인함수이면 실행 
if __name__ == "__main__":

    db = pymysql.connect(host='localhost', port=3306, user='root', passwd='yoy0317689*', db='snowball_database', charset='utf8') 
    snowball=db.cursor() 

    backtest_object = backtest('123456', 'test', 1000000, [40,60], '2017-10-01', '2018-05-01', 3, 0, 600000)

    backtest_object.do_backtest()
    db.close()  