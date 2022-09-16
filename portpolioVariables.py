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

def get_portVariables(dict_realvalue, dict_inputmoney):
    portfolio_result = dict()
    values = dict()
    for key in dict_inputmoney.keys():
        values[key] = list()
        values[key].append(float(dict_inputmoney[key]))
        values[key].append(dict_realvalue[key])

    df = pd.DataFrame.from_dict(values, orient='index', columns=['seed', 'value'])  # 넘겨받은 사전 데이터 데이터프레임으로 변환

    get_returns(df)  # 수익률 계산
    win_rate = get_winRate(df)  # 승률 계산해서 저장 (리밸런싱 날짜 기준)
    mdd = get_mdd(df)  # mdd 계산
    # print(df)
    # print("승률: ", win_rate, "%")
    # print(mdd)
    # print(df['return'].to_dict())
    portfolio_result['승률'] = win_rate
    portfolio_result['MDD'] = mdd
    portfolio_result['수익률'] = dict(zip(df.index, df['return']))
    portfolio_result['포트폴리오 가치'] = df.iloc[-1, 1]  # 포트폴리오 가치 저장, 초기값: 수령 직전 가치
    portfolio_result['누적 수익률'] = df.iloc[-1, 2]
    portfolio_result['월 수익률 추이'] = monthlyReturn(real_portfolio_account)

    return portfolio_result


def get_returns(df):
    df['return'] = (df['value'] - df['seed']) / df['seed']  # +df['cash'] #일별수익률 계산해서 열 추가 (월간수익률(납입일 기준),추가 가능)
    df['return'] = df['return'].round(2)


def monthlyReturn(dict_realvalue):
    # 입력: 포트폴리오 가치
    realValue = dict()
    rtDict = dict()
    realValue = dict_realvalue
    mfValue = realValue[next(iter(realValue))]  # 월 초 가치, 초기값: 시작 날 가치
    mlValue = realValue[next(iter(realValue))]  # 월 말 가치
    month = next(iter(realValue))
    firstmonth = month.split('-')[1]
    ymonth = month.split('-')[0] + '-' + month.split('-')[1]
    monthCount = 1

    keyList = []
    for key in realValue.keys():
        keyList.append(key)

    for i in range(len(keyList)):
        splitkey = keyList[i].split('-')
        mlValue = realValue[keyList[i - 1]]  # 월 말 value 보존
        if (splitkey[1] != firstmonth):  # 월 변경될 경우
            rtDict[ymonth] = round((mlValue - mfValue) / mfValue * 100, 2)  # 월 수익률 계산
            mfValue = realValue[keyList[i]]  # 월 초 값 갱신
            ymonth = splitkey[0] + "-" + splitkey[1]  # 연-월 갱신 (딕셔너리 생성에 사용)
            firstmonth = splitkey[1]  # 월 갱신 (월 비교에 사용)
            monthCount = monthCount + 1  # 운용 개월 수 체크

        rtDict[ymonth] = round((realValue[key] - mfValue) / mfValue * 100, 2)  # realValue[key]: 마지막 날 수익률 마지막 달 수익률 계산

    sum_MonthlyReturn = 0
    for key in rtDict.keys():
        sum_MonthlyReturn = sum_MonthlyReturn + rtDict[key]

    rtDict['월 수익률 평균'] = round(sum_MonthlyReturn / monthCount, 2)

    return (rtDict)


def get_winRate(df):
    # 리밸런싱 날짜 리스트받아서, 해당하는 날짜들의 승률 계산해서 반환
    win_count = 0

    for i in df.index:
        if df.loc[i, 'return'] >= 0:
            win_count = win_count + 1

    return round((win_count) / (len(df.index)) * 100, 2)


def get_mdd(df):
    # MDD(Maximum Draw-Down): 기간 내 최대 낙폭
    #:return: (peak_upper, peak_lower, mdd_rate) v

    arr_v = np.array(df['return'])
    peak_lower = np.argmax(np.maximum.accumulate(arr_v) - arr_v)
    peak_upper = np.argmax(arr_v[:peak_lower])
    mdd = round((arr_v[peak_lower] - arr_v[peak_upper]) / arr_v[peak_upper], 2)
    return df.index[peak_upper], df.index[peak_lower], mdd  # (기간 최저) - (기간 최고) / (기간 최고) -> 기간 내 최대 낙폭


def receipt_simul(portfolioResult, receiptYear):
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

    rtDict1 = dict()
    rtDict1['총 수령액'] = 0
    can_receiptValue = 0

    for i in range(1, receiptYear + 1):
        can_receiptValue = int(cum_value / (receiptYear - (i - 1)))  # 남은 금액을 남은 연차로 엔빵
        if i <= 10:  # 1~10년차의 경우
            if can_receiptValue > cal_receiptValue(i, cum_value):
                can_receiptValue = int(cal_receiptValue(i, cum_value))  # 10년이내의 최대를 넘을 시 최대금액으로 제한
        if can_receiptValue > 12000000:  # 세액공제 한도 초과 시
            can_receiptValue = 12000000  # 한도 범위인 1200만원으로 제한
        cum_value = int(cum_value - can_receiptValue)  # 잔액 정리
        rtDict1[str(i) + '년차 수령금액'] = can_receiptValue
        rtDict1['총 수령액'] = rtDict1['총 수령액'] + can_receiptValue

    rtDict1['잔액'] = cum_value

    cum_value2 = int(portfolioResult['포트폴리오 가치'])  # 포트폴리오 가치 저장, 초기값: 수령 직전 가치
    rtDict2 = dict()
    rtDict2['총 수령액'] = 0
    can_receiptValue2 = 0
    year = 1

    while cum_value2 > 0:
        if year <= 10:
            can_receiptValue2 = int(cal_receiptValue(year, cum_value2))  # 당 해 수령가능 금액
        else:
            can_receiptValue2 = int(cum_value2)

        if can_receiptValue2 > 12000000:
            can_receiptValue2 = 12000000

        rtDict2[str(year) + '년차 수령금액'] = can_receiptValue2
        rtDict2['총 수령액'] = rtDict2['총 수령액'] + can_receiptValue2
        cum_value2 = int(cum_value2 - can_receiptValue2)
        year = year + 1

    rtDict2['잔액'] = cum_value2

    # print("수령방식: ", receiptWay)
    # print()
    # print("포트폴리오 누적 가치: ", cum_value)
    # print()
    # print("수익률 평균: ", mean_return)

    if rtDict1['잔액'] > 0:
        print("첫 번째 방식의 경우 잔액이 0보다 큽니다, 수령 기간을 늘리시길 권장드립니다.")
    rtList = [rtDict1, rtDict2]
    return rtList


def cal_receiptValue(year, value):
    if year == 10:
        return value

    return value / (11 - year) * 1.2

# print(get_portVariables(real_portfolio_account, input_money_to_portfolio))
