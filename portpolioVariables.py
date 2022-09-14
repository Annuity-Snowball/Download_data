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

values= {'2021-01-01': [1000000.0, 949528.0],'2021-01-10': [1000000.0, 512878.0], '2021-01-15': [1000000.0, 1112878.0], '2021-02-01': [1500000.0, 1646600.0], '2021-02-15': [1500000.0, 1533469.0],
          '2021-03-01': [2000000.0, 2203818.0], '2021-03-15': [2000000.0, 1974316.0], '2021-04-01': [2500000.0, 2101941.0], '2021-04-15': [2500000.0, 2464465.0],
          '2021-05-01': [3000000.0, 2450307.0], '2021-05-15': [3000000.0, 3001719.0], '2021-06-01': [3500000.0, 3626080.0]}
        # '2021-01-10'의 경우 MDD테스트를 위한 임의값

rebalanceTestList = ['2021-01-01', '2021-02-01', '2021-03-01', '2021-04-01', '2021-05-01', '2021-06-01' ] #승률 계산을 위한 임시 리밸런싱 날짜 리스트

# 누적수익률
# gross_ret = df['return']+1
# df['cum_ret'] = gross_ret.cumprod() - 1

def get_portVariables(df):
    df = pd.DataFrame.from_dict(values, orient='index', columns=['seed', 'value']) #넘겨받은 사전 데이터 데이터프레임으로 변환
    df['seed_val_ratio'] = df['value'] / df['seed']                                #원금 / 수익 비율 계산해서 열 추가

    get_returns(df) # 수익률 계산
    win_rate = get_winRate(df, rebalanceTestList) # 승률 계산해서 저장 (리밸런싱 날짜 기준)
    mdd = get_mdd(df) #mdd 계산
    print(df)
    print("승률: ", win_rate, "%")
    print("mdd: ", mdd)

    receipt_simul(df)
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