import datetime
import pandas as pd
import numpy as np
import datetime as dt
from pandas.tseries.offsets import *
from pandas_datareader import data as pdr

# 수익률: ((당일 가치) -(원금) + (현금)) / (원금) -> return column
# MDD: 특정 기간동안 발생한 최대 낙폭 = (기간동안의 최저점 - 기간동안의 최고점) / 기간동안의 최고점
# 승률: 리밸런싱일 기준으로 계산
# 연최고 수익률: return column의 max value
# 연최저 수익률: return column의 min value

real_portfolio_account = {'2020-01-02': 1000000.0, '2020-01-03': 1084857.0, '2020-01-06': 1112886.0, '2020-01-07': 1073335.0, '2020-01-08': 1095511.0, '2020-01-09': 1066335.0, '2020-01-10': 1214549.0, '2020-01-13': 1035767.0, '2020-01-14': 996590.0, '2020-01-15': 995886.0, '2020-01-16': 1091930.0, '2020-01-17': 953594.0, '2020-01-20': 1076332.0, '2020-01-21': 853594.0, '2020-01-22': 1103614.0, '2020-01-23': 995810.0, '2020-01-28': 1030037.0, '2020-01-29': 1178249.0, '2020-01-30': 1132974.0, '2020-01-31': 1150342.0, '2020-02-03': 1707516.0, '2020-02-04': 1717542.0, '2020-02-05': 1598419.0, '2020-02-06': 1556958.0, '2020-02-07': 1752117.0, '2020-02-10': 1578963.0, '2020-02-11': 1550351.0, '2020-02-12': 1402428.0, '2020-02-13': 1638759.0, '2020-02-14': 1668205.0, '2020-02-17': 1380301.0, '2020-02-18': 1646733.0, '2020-02-19': 1611243.0, '2020-02-20': 1486234.0, '2020-02-21': 1592605.0, '2020-02-24': 1487701.0, '2020-02-25': 1229660.0, '2020-02-26': 1439640.0, '2020-02-27': 1662007.0, '2020-02-28': 1433545.0, '2020-03-02': 2098338.0, '2020-03-03': 2036651.0, '2020-03-04': 1739071.0, '2020-03-05': 2075277.0, '2020-03-06': 2115119.0, '2020-03-09': 2073672.0, '2020-03-10': 1719805.0, '2020-03-11': 2241268.0, '2020-03-12': 2176451.0, '2020-03-13': 2308126.0, '2020-03-16': 2088967.0, '2020-03-17': 1920055.0, '2020-03-18': 2067868.0, '2020-03-19': 2300216.0, '2020-03-20': 1934926.0, '2020-03-23': 1954825.0, '2020-03-24': 2381138.0, '2020-03-25': 2486455.0, '2020-03-26': 1984225.0, '2020-03-27': 2201030.0, '2020-03-30': 1961189.0, '2020-03-31': 2130836.0, '2020-04-01': 2630835.0, '2020-04-02': 2866307.0, '2020-04-03': 2746908.0, '2020-04-06': 2519362.0, '2020-04-07': 2447943.0, '2020-04-08': 2752478.0, '2020-04-09': 3140109.0, '2020-04-10': 2625241.0, '2020-04-13': 2619421.0, '2020-04-14': 2929484.0, '2020-04-16': 2947966.0, '2020-04-17': 3230063.0, '2020-04-20': 2947982.0, '2020-04-21': 2597812.0, '2020-04-22': 3222738.0, '2020-04-23': 2838693.0, '2020-04-24': 2884845.0, '2020-04-27': 2804201.0, '2020-04-28': 2528824.0, '2020-04-29': 2663447.0, '2020-05-04': 3265332.0, '2020-05-06': 3561894.0, '2020-05-07': 3349892.0, '2020-05-08': 3154992.0, '2020-05-11': 3117888.0, '2020-05-12': 3248682.0, '2020-05-13': 3643630.0, '2020-05-14': 3298872.0, '2020-05-15': 3368778.0, '2020-05-18': 3147618.0, '2020-05-19': 2957766.0, '2020-05-20': 2921044.0, '2020-05-21': 3434534.0, '2020-05-22': 2915614.0, '2020-05-25': 3194406.0, '2020-05-26': 2919550.0, '2020-05-27': 3084944.0, '2020-05-28': 3472746.0, '2020-05-29': 3459934.0, '2020-06-01': 4234662.0, '2020-06-02': 3570540.0, '2020-06-03': 3998466.0, '2020-06-04': 4307449.0, '2020-06-05': 3900067.0, '2020-06-08': 3347737.0, '2020-06-09': 3991037.0, '2020-06-10': 3664077.0, '2020-06-11': 4269264.0, '2020-06-12': 3403682.0, '2020-06-15': 4239198.0, '2020-06-16': 3456169.0, '2020-06-17': 3944308.0, '2020-06-18': 3818354.0, '2020-06-19': 3764217.0, '2020-06-22': 3495238.0, '2020-06-23': 3316322.0, '2020-06-24': 4059224.0, '2020-06-25': 3125178.0, '2020-06-26': 3984110.0, '2020-06-29': 4107606.0, '2020-06-30': 3332387.0, '2020-07-01': 3832385.0, '2020-07-02': 4390202.0, '2020-07-03': 4450005.0, '2020-07-06': 4331083.0, '2020-07-07': 4473669.0, '2020-07-08': 3593808.0, '2020-07-09': 4734951.0, '2020-07-10': 4395348.0, '2020-07-13': 3837733.0, '2020-07-14': 4748803.0, '2020-07-15': 4824585.0, '2020-07-16': 4716874.0, '2020-07-17': 5219423.0, '2020-07-20': 4719355.0, '2020-07-21': 4247424.0, '2020-07-22': 4943353.0, '2020-07-23': 4475238.0, '2020-07-24': 5070813.0, '2020-07-27': 5163225.0, '2020-07-28': 3987836.0, '2020-07-29': 4105264.0, '2020-07-30': 4008446.0, '2020-07-31': 4007092.0}

input_money_to_portfolio = {'2020-01-02': 500000, '2020-01-03': 500000, '2020-01-06': 500000, '2020-01-07': 500000, '2020-01-08': 500000, '2020-01-09': 500000, '2020-01-10': 500000, '2020-01-13': 500000, '2020-01-14': 500000, '2020-01-15': 500000, '2020-01-16': 500000, '2020-01-17': 500000, '2020-01-20': 500000, '2020-01-21': 500000, '2020-01-22': 500000, '2020-01-23': 500000, '2020-01-28': 500000, '2020-01-29': 500000, '2020-01-30': 500000, '2020-01-31': 500000, '2020-02-03': 1000000, '2020-02-04': 1000000, '2020-02-05': 1000000, '2020-02-06': 1000000, '2020-02-07': 1000000, '2020-02-10': 1000000, '2020-02-11': 1000000, '2020-02-12': 1000000, '2020-02-13': 1000000, '2020-02-14': 1000000, '2020-02-17': 1000000, '2020-02-18': 1000000, '2020-02-19': 1000000, '2020-02-20': 1000000, '2020-02-21': 1000000, '2020-02-24': 1000000, '2020-02-25': 1000000, '2020-02-26': 1000000, '2020-02-27': 1000000, '2020-02-28': 1000000, '2020-03-02': 1500000, '2020-03-03': 1500000, '2020-03-04': 1500000, '2020-03-05': 1500000, '2020-03-06': 1500000, '2020-03-09': 1500000, '2020-03-10': 1500000, '2020-03-11': 1500000, '2020-03-12': 1500000, '2020-03-13': 1500000, '2020-03-16': 1500000, '2020-03-17': 1500000, '2020-03-18': 1500000, '2020-03-19': 1500000, '2020-03-20': 1500000, '2020-03-23': 1500000, '2020-03-24': 1500000, '2020-03-25': 1500000, '2020-03-26': 1500000, '2020-03-27': 1500000, '2020-03-30': 1500000, '2020-03-31': 1500000, '2020-04-01': 2000000, '2020-04-02': 2000000, '2020-04-03': 2000000, '2020-04-06': 2000000, '2020-04-07': 2000000, '2020-04-08': 2000000, '2020-04-09': 2000000, '2020-04-10': 2000000, '2020-04-13': 2000000, '2020-04-14': 2000000, '2020-04-16': 2000000, '2020-04-17': 2000000, '2020-04-20': 2000000, '2020-04-21': 2000000, '2020-04-22': 2000000, '2020-04-23': 2000000, '2020-04-24': 2000000, '2020-04-27': 2000000, '2020-04-28': 2000000, '2020-04-29': 2000000, '2020-05-04': 2500000, '2020-05-06': 2500000, '2020-05-07': 2500000, '2020-05-08': 2500000, '2020-05-11': 2500000, '2020-05-12': 2500000, '2020-05-13': 2500000, '2020-05-14': 2500000, '2020-05-15': 2500000, '2020-05-18': 2500000, '2020-05-19': 2500000, '2020-05-20': 2500000, '2020-05-21': 2500000, '2020-05-22': 2500000, '2020-05-25': 2500000, '2020-05-26': 2500000, '2020-05-27': 2500000, '2020-05-28': 2500000, '2020-05-29': 2500000, '2020-06-01': 3000000, '2020-06-02': 3000000, '2020-06-03': 3000000, '2020-06-04': 3000000, '2020-06-05': 3000000, '2020-06-08': 3000000, '2020-06-09': 3000000, '2020-06-10': 3000000, '2020-06-11': 3000000, '2020-06-12': 3000000, '2020-06-15': 3000000, '2020-06-16': 3000000, '2020-06-17': 3000000, '2020-06-18': 3000000, '2020-06-19': 3000000, '2020-06-22': 3000000, '2020-06-23': 3000000, '2020-06-24': 3000000, '2020-06-25': 3000000, '2020-06-26': 3000000, '2020-06-29': 3000000, '2020-06-30': 3000000, '2020-07-01': 3500000, '2020-07-02': 3500000, '2020-07-03': 3500000, '2020-07-06': 3500000, '2020-07-07': 3500000, '2020-07-08': 3500000, '2020-07-09': 3500000, '2020-07-10': 3500000, '2020-07-13': 3500000, '2020-07-14': 3500000, '2020-07-15': 3500000, '2020-07-16': 3500000, '2020-07-17': 3500000, '2020-07-20': 3500000, '2020-07-21': 3500000, '2020-07-22': 3500000, '2020-07-23': 3500000, '2020-07-24': 3500000, '2020-07-27': 3500000, '2020-07-28': 3500000, '2020-07-29': 3500000, '2020-07-30': 3500000, '2020-07-31': 3500000}

values = dict()


for key in input_money_to_portfolio.keys():
    values[key]=list()
    values[key].append(input_money_to_portfolio[key])
    values[key].append(real_portfolio_account[key])
    


values= {'2021-01-01': [1000000.0, 949528.0],'2021-01-10': [1000000.0, 512878.0], '2021-01-15': [1000000.0, 1112878.0], '2021-02-01': [1500000.0, 1646600.0], '2021-02-15': [1500000.0, 1533469.0],
          '2021-03-01': [2000000.0, 2203818.0], '2021-03-15': [2000000.0, 1974316.0], '2021-04-01': [2500000.0, 2101941.0], '2021-04-15': [2500000.0, 2464465.0],
          '2021-05-01': [3000000.0, 2450307.0], '2021-05-15': [3000000.0, 3001719.0], '2021-06-01': [3500000.0, 3626080.0]}
        # '2021-01-10'의 경우 MDD테스트를 위한 임의값

rebalanceTestList = ['2021-01-01', '2021-02-01', '2021-03-01', '2021-04-01', '2021-05-01', '2021-06-01' ] #승률 계산을 위한 임시 리밸런싱 날짜 리스트

# 누적수익률
# gross_ret = df['return']+1
# df['cum_ret'] = gross_ret.cumprod() - 1

def get_portVariables(df):
    portfolio_result = dict()
    df = pd.DataFrame.from_dict(values, orient='index', columns=['seed', 'value']) #넘겨받은 사전 데이터 데이터프레임으로 변환
    df['seed_val_ratio'] = df['value'] / df['seed']                                #원금 / 수익 비율 계산해서 열 추가

    get_returns(df) # 수익률 계산
    win_rate = get_winRate(df, rebalanceTestList) # 승률 계산해서 저장 (리밸런싱 날짜 기준)
    mdd = get_mdd(df) #mdd 계산
    print(df)
    print("승률: ", win_rate, "%")
    print("mdd: ", mdd)
    portfolio_result['승률']=win_rate
    portfolio_result['mdd']=mdd
    portfolio_result['수익률'] = list(df['return'])
    return portfolio_result
    
    
    
    
def get_returns(df):
    df['return'] = (df['value'] - df['seed']) / df['seed']  # +df['cash'] #일별수익률 계산해서 열 추가 (월간수익률(납입일 기준),추가 가능)

def get_winRate(df, rebalace_dateInfoList):
    #리밸런싱 날짜 리스트받아서, 해당하는 날짜들의 승률 계산해서 반환
    win_count = 0

    for i in rebalace_dateInfoList:
        if df.loc[i, 'return'] >= 0:
            win_count = win_count + 1

    return (win_count) / (len(rebalace_dateInfoList)) * 100


def get_mdd(df):
    #MDD(Maximum Draw-Down): 기간 내 최대 낙폭
    #:return: (peak_upper, peak_lower, mdd_rate) v

    window = 12  # 기간 = 12납입일(임시)
    max_in_seedValratio = df['seed_val_ratio'].rolling(window, min_periods=1).max()  # 기간동안의 최댓값 저장
    dd = ((df['seed_val_ratio']) / max_in_seedValratio - 1.0) * 100  # DD: 현재값/최댓값(기간) - 1
    mdd = dd.rolling(window, min_periods=1).min()  # 기간 내 DD중 최솟값
    print("임시계산: ",mdd) #임시 출력

    arr_v = np.array(df['seed_val_ratio'])
    peak_lower = np.argmax(np.maximum.accumulate(arr_v) - arr_v)
    peak_upper = np.argmax(arr_v[:peak_lower])
    return peak_upper, peak_lower, (arr_v[peak_lower] - arr_v[peak_upper]) / arr_v[peak_upper] # (기간 최저) - (기간 최고) / (기간 최고) -> 기간 내 최대 낙폭

def receipt_simul(df):
    #수령 시뮬레이션
    #연간 수령한도: 계좌평가액 / (11 - 연금수령연차) * 1.2 -> 1년간 자유롭게 나누어 수령 가능 (수령하지 않는 것도 가능) - 매년 1월 1일 기준으로 평가
    #연 1,200만원 이상 수령 시, 종합소득세 부과 (16.5%)
    # 수령 가능금액 확인
    # 1. 정량수령 2. 정률수령 3.자율수령 선택
    # 수령 금액 결정
    # (수령 후 금액) = (잔액 x 포트폴리오 평균수익률)

    print("연금 수령방식 선택")
    print("1: 정액수령(월)")
    print("2: 비율수령(월)")
    print("3: 자율수령: " )

    receiptWay = int(input())  # 수령방식
    cum_value = df.iloc[-1, 1] # 포트폴리오 가치 저장, 초기값: 수령 직전 가치
    mean_return = df['return'].mean() # 수익률 평균


    if receiptWay == 1:
        for i in range(1, 11): #10년 이후부터는 한도x
            can_receiptValue = cal_receiptValue(i, cum_value) # 연간 수령가능 금액
            print(i, "년차 수령 가능금액: ", can_receiptValue)


            print("매 월 수령할 금액 입력(최대 ", can_receiptValue/12, "원)")
            print(": ")
            while(1):
                monthlyReceipt = int(input())           # 월간 수령금액 입력받기
                if monthlyReceipt > can_receiptValue:
                    print("금액 초과, 재입력: ")
                    continue
                break
            print(i, "년차 수령금액: ", monthlyReceipt * 12)
            cum_value = int((cum_value - monthlyReceipt * 12)*(1+mean_return)) # 누적금액 갱신, 수령한 만큼 제하기

        print("10년 수령 후 계좌 잔액: ", cum_value)


    elif receiptWay == 2:
        print("수령가능금액 중 매 년 수령할 비율을 입력(최대 100%)")
        print(": ")
        while (1):
            yearlyReceiptRatio = int(input())  # 월간 수령금액 입력받기
            if yearlyReceiptRatio > 100 or yearlyReceiptRatio < 0:
                print("허용되지 않은 값, 재입력: ")
                continue
            break


        for i in range(1, 11):  # 10년 이후부터는 한도x
            can_receiptValue = cal_receiptValue(i, cum_value)  # 연간 수령가능 금액
            print(i, "년차 수령금액: ", int(can_receiptValue * yearlyReceiptRatio / 100))
            cum_value = int((cum_value - can_receiptValue * yearlyReceiptRatio / 100)*(1+mean_return))  # 누적금액 갱신, 수령한 만큼 제하기

        print("10년 수령 후 계좌 잔액: ", cum_value)

    elif receiptWay == 3:
        for i in range(1, 11): #10년 이후부터는 한도x
            can_receiptValue = cal_receiptValue(i, cum_value) # 연간 수령가능 금액
            print(i, "년차 수령 가능금액: ", can_receiptValue)

            print(i, " 년차에 수령하실 금액을 입력하세요(최대 ", can_receiptValue, "원)")
            print(": ")
            while(1):
                Receipt = int(input())           # 연 수령금액 입력받기
                if Receipt > can_receiptValue:
                    print("금액 초과, 재입력: ")
                    continue
                break
            print(i, "년차 수령금액: ", Receipt)
            cum_value = int((cum_value - Receipt)*(1+mean_return)) # 누적금액 갱신, 수령한 만큼 제하기

        print("10년 수령 후 계좌 잔액: ", cum_value)
    else:
        pass

    # print("수령방식: ", receiptWay)
    # print()
    # print("포트폴리오 누적 가치: ", cum_value)
    # print()
    # print("수익률 평균: ", mean_return)
def cal_receiptValue(year, value):

    if year == 10:
        return value

    return value / (11 - year) * 1.2

# get_portVariables(values) #합본함수 실행