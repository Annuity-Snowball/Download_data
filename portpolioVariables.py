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
    portfolio_result['승률'] = win_rate
    portfolio_result['MDD'] = mdd
    portfolio_result['수익률'] = list(df['return'].to_dict())
    portfolio_result['포트폴리오 가치'] = df.iloc[-1, 1]  # 포트폴리오 가치 저장, 초기값: 수령 직전 가치
    portfolio_result['운용 평균 수익률'] = df['return'].mean()
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

    return round((win_count) / (len(rebalace_dateInfoList)) * 100, 2)


def get_mdd(df):
    # MDD(Maximum Draw-Down): 기간 내 최대 낙폭
    #:return: (peak_upper, peak_lower, mdd_rate) v

    arr_v = np.array(df['return'])
    peak_lower = np.argmax(np.maximum.accumulate(arr_v) - arr_v)
    peak_upper = np.argmax(arr_v[:peak_lower])
    mdd = round((arr_v[peak_lower] - arr_v[peak_upper]) / arr_v[peak_upper], 2)
    return df.index[peak_upper], df.index[peak_lower], mdd  # (기간 최저) - (기간 최고) / (기간 최고) -> 기간 내 최대 낙폭


def receipt_simul(portfolioResult, receiptWay, receiptYear=None):
    # 수령 시뮬레이션
    # 연간 수령한도: 계좌평가액 / (11 - 연금수령연차) * 1.2 -> 1년간 자유롭게 나누어 수령 가능 (수령하지 않는 것도 가능) - 매년 1월 1일 기준으로 평가
    # 연 1,200만원 이상 수령 시, 종합소득세 부과 (16.5%)
    # 수령 가능금액 확인
    # 0: 수령 시 운용 중지
    # 1: 수령 시 운용 유지
    # (수령 후 다음 해 잔액) = (잔액 x 포트폴리오 기간 내 평균수익률)

    cum_value = int(portfolioResult['포트폴리오 가치'])  # 포트폴리오 가치 저장, 초기값: 수령 직전 가치
    # print("수령 직전가치: ", cum_value)
    # print("평균수익률: ", mean_return)

    rtDict = dict()
    rtDict['총 수령액'] = 0
    can_receiptValue = 0

    if receiptWay == 0:  # receiptYear동안 최대로 받기
        for i in range(1, receiptYear + 1):
            can_receiptValue = int(cum_value / (receiptYear - (i - 1)))  # 남은 금액을 남은 연차로 엔빵
            if i <= 10:  # 1~10년차의 경우
                if can_receiptValue > cal_receiptValue(i, cum_value):
                    can_receiptValue = int(cal_receiptValue(i, cum_value))  # 10년이내의 최대를 넘을 시 최대금액으로 제한
            if can_receiptValue > 12000000:  # 세액공제 한도 초과 시
                can_receiptValue = 12000000  # 한도 범위인 1200만원으로 제한
            cum_value = int(cum_value - can_receiptValue)  # 잔액 정리
            rtDict[str(i) + '년차 수령금액'] = can_receiptValue
            rtDict['총 수령액'] = rtDict['총 수령액'] + can_receiptValue

    rtDict['잔액'] = cum_value

    if receiptWay == 1:  # 매년 최대 금액으로 몇 년 받을 수 있니?

        year = 1

        while cum_value > 0:
            if year <= 10:
                can_receiptValue = int(cal_receiptValue(year, cum_value))  # 당 해 수령가능 금액
            else:
                can_receiptValue = int(cum_value)

            if can_receiptValue > 12000000:
                can_receiptValue = 12000000

            rtDict[str(year) + '년차 수령금액'] = can_receiptValue
            rtDict['총 수령액'] = rtDict['총 수령액'] + can_receiptValue
            cum_value = int(cum_value - can_receiptValue)
            year = year + 1

        rtDict['잔액'] = cum_value

        # can_receiptValue = int(cal_receiptValue(1, cum_value))  # 첫 해 수령가능 금액

        # while (1):
        #     # print("매 월 수령할 금액 입력(최대 ", int(can_receiptValue / 12), "원): ")
        #     monthlyReceipt = int(input())  # 월간 수령금액 입력받기
        #     if monthlyReceipt > int(can_receiptValue / 12):  # 입력값이 수령 가능범위를 넘는 경우
        #         print("금액 한도 초과, 재입력: ")
        #         continue
        #     break
        #
        # receiptMonth = int(cum_value / monthlyReceipt)  # 수령 개월 수
        # rtDict['수령 개월 수'] = receiptMonth
        #
        #
        # for i in range(receiptMonth): # 10년 이후부터는 한도x
        #     rtDict['총 수령액'] = rtDict['총 수령액'] + monthlyReceipt
        #     cum_value = int(cum_value - monthlyReceipt)
        #
        # rtDict['수령 후 잔액'] = cum_value
        # print(rtDict)

    # elif receiptWay == 1: #운용 x, 매 년 최대 금액 및 1200만원 제한 -> 10년 고정으로 수령하게 되어있음.
    #     for i in range(1, 11):
    #         can_receiptValue = int(cal_receiptValue(i, cum_value))  # 해마다 수령 가능금액
    #         if can_receiptValue > 12000000:
    #             can_receiptValue = 12000000 # 최대 연 1200만원 제한
    #         rtDict[str(i) + '년차 수령액'] = can_receiptValue
    #         rtDict['총 수령액'] = rtDict['총 수령액'] + can_receiptValue
    #         cum_value = int(cum_value - can_receiptValue)
    #
    #     rtDict['수령 후 잔액'] = cum_value
    #     print(rtDict)
    #
    if (rtDict['잔액'] > 0):
        print("잔액이 0보다 큽니다, 수령 기간을 늘리시길 권장드립니다.")
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
