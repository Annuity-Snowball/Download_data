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



# 누적수익률
# gross_ret = df['return']+1
# df['cum_ret'] = gross_ret.cumprod() - 1

def get_portVariables(dict_realvalue, dict_inputmoney, rebalanceDateList):
    portfolio_result = dict()
    values = dict()
    for key in dict_inputmoney.keys():
        values[key] = list()
        values[key].append(float(dict_inputmoney[key]))
        values[key].append(dict_realvalue[key])

    df = pd.DataFrame.from_dict(values, orient='index', columns=['seed', 'value'])  # 넘겨받은 사전 데이터 데이터프레임으로 변환

    get_returns(df)  # 수익률 계산
    win_rate = get_winRate(df, rebalanceDateList)  # 승률 계산해서 저장 (리밸런싱 날짜 기준)
    mdd = get_mdd(df)  # mdd 계산
    # print(df)
    # print("승률: ", win_rate, "%")
    # print(mdd)
    # print(df['return'].to_dict())
    portfolio_result['win_rate'] = win_rate
    portfolio_result['mdd'] = mdd
    portfolio_result['return'] = list(df['return'].to_dict())
    portfolio_result['current_value'] = df.iloc[-1, 1]  # 포트폴리오 가치 저장, 초기값: 수령 직전 가치
    portfolio_result['mean_return'] = df['return'].mean()
    return portfolio_result


def get_returns(df):
    df['return'] = (df['value'] - df['seed']) / df['seed']  # +df['cash'] #일별수익률 계산해서 열 추가 (월간수익률(납입일 기준),추가 가능)
    df['return'] = df['return'].round(2)
def get_winRate(df, rebalace_dateInfoList):
    # 리밸런싱 날짜 리스트받아서, 해당하는 날짜들의 승률 계산해서 반환
    win_count = 0

    for i in rebalace_dateInfoList:
        if df.loc[i, 'return'] >= 0:
            win_count = win_count + 1

    return (win_count) / (len(rebalace_dateInfoList)) * 100


def get_mdd(df):
    # MDD(Maximum Draw-Down): 기간 내 최대 낙폭
    #:return: (peak_upper, peak_lower, mdd_rate) v

    arr_v = np.array(df['return'])
    peak_lower = np.argmax(np.maximum.accumulate(arr_v) - arr_v)
    peak_upper = np.argmax(arr_v[:peak_lower])
    mdd = round((arr_v[peak_lower] - arr_v[peak_upper]) / arr_v[peak_upper], 2)
    return df.index[peak_upper], df.index[peak_lower],mdd   # (기간 최저) - (기간 최고) / (기간 최고) -> 기간 내 최대 낙폭


def receipt_simul(portfolioResult, receiptWay):
    # 수령 시뮬레이션
    # 연간 수령한도: 계좌평가액 / (11 - 연금수령연차) * 1.2 -> 1년간 자유롭게 나누어 수령 가능 (수령하지 않는 것도 가능) - 매년 1월 1일 기준으로 평가
    # 연 1,200만원 이상 수령 시, 종합소득세 부과 (16.5%)
    # 수령 가능금액 확인
    # 0: 정량수령
    # 1: 정률수령
    # 2: 자율수령 선택
    # 수령 금액 결정
    # (수령 후 다음 해 잔액) = (잔액 x 포트폴리오 기간 내 평균수익률)

    cum_value = portfolioResult['current_value']  # 포트폴리오 가치 저장, 초기값: 수령 직전 가치
    # print("수령 직전가치: ", cum_value)
    mean_return = round(portfolioResult['mean_return'], 2)
    # print("평균수익률: ", mean_return)

    rtDict = dict()

    if receiptWay == 0:
        can_receiptValue = cal_receiptValue(1, cum_value)  # 첫 해 수령가능 금액

        while (1):
            print("매 월 수령할 금액 입력(최대 ", int(can_receiptValue / 12), "원): ")
            monthlyReceipt = int(input())  # 월간 수령금액 입력받기
            if monthlyReceipt > int(can_receiptValue / 12):  # 입력값이 수령 가능범위를 넘는 경우
                print("금액 한도 초과, 재입력: ")
                continue
            break

        for i in range(1, 11):  # 10년 이후부터는 한도x

            rtDict[i] = int(monthlyReceipt * 12)
            cum_value = int((cum_value - monthlyReceipt * 12) * (1 + mean_return))  # 누적금액 갱신, 수령한 만큼 제하기

        rtDict['leftMoney'] = cum_value

    elif receiptWay == 1:
        print("수령가능금액 중 매 년 수령할 비율을 입력(최대 100%): ")
        while (1):
            yearlyReceiptRatio = int(input())  # 월간 수령금액 입력받기
            if yearlyReceiptRatio > 100 or yearlyReceiptRatio < 0:
                print("허용되지 않은 값, 재입력: ")
                continue
            break

        for i in range(1, 11):  # 10년 이후부터는 한도x
            can_receiptValue = int(cal_receiptValue(i, cum_value))  # 연간 수령가능 금액
            rtDict[i] = int(can_receiptValue * yearlyReceiptRatio / 100)
            cum_value = int(
                (cum_value - can_receiptValue * yearlyReceiptRatio / 100) * (1 + mean_return))  # 누적금액 갱신, 수령한 만큼 제하기

        rtDict['leftMoney'] = cum_value

    elif receiptWay == 2:
        for i in range(1, 11):  # 10년 이후부터는 한도x
            can_receiptValue = int(cal_receiptValue(i, cum_value))  # 연간 수령가능 금액

            print(i, " 년차에 수령하실 금액을 입력하세요(최대 ", can_receiptValue, "원): ")
            while (1):
                Receipt = int(input())  # 연 수령금액 입력받기
                if Receipt > can_receiptValue:
                    print("금액 초과, 재입력: ")
                    continue
                break
            rtDict[i] = Receipt
            cum_value = int((cum_value - Receipt) * (1 + mean_return))  # 누적금액 갱신, 수령한 만큼 제하기

        rtDict['leftMoney']  = cum_value

    return rtDict

    # print("수령방식: ", receiptWay)
    # print()
    # print("포트폴리오 누적 가치: ", cum_value)
    # print()
    # print("수익률 평균: ", mean_return)


def cal_receiptValue(year, value):
    if year == 10:
        return value

    return value / (11 - year) * 1.2


