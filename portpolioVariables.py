import datetime

import yfinance as yf
import pandas as pd
import numpy as np
import datetime as dt
from pandas.tseries.offsets import *
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from mpl_finance import candlestick_ohlc

# 일별 수익률: (오늘종가 - 어제 종가) / (어제 종가) -1 의 가중평균

values = {'2021-01-01': 949528.0, '2021-01-15': 1112878.0, '2021-02-01': 1646600.0, '2021-02-15': 1533469.0,
          '2021-03-01': 2203818.0, '2021-03-15': 1974316.0, '2021-04-01': 2101941.0, '2021-04-15': 2464465.0,
          '2021-05-01': 2450307.0, '2021-05-15': 3001719.0, '2021-06-01': 3626080.0}

df = pd.DataFrame.from_dict(values, orient='index', columns=['value'])
print(df)
daily_ret = df.pct_change(1).dropna()
print(daily_ret)

gross_ret = daily_ret+1
cum_ret = gross_ret.cumprod() - 1
print(cum_ret)

# 포트폴리오 -> 가중평균으로 구하기 ex) 상품a $100, 상품b $200 -> 1/3, 2/3 가중치로 계산하여 평균 구하기

# MDD : 특정 기간동안 발생한 최대 낙폭 = (기간동안의 최저점 - 기간동안의 최고점) / 기간동안의 최고점 -> 종목별로 구해서 가중평균내기
# 승률 : 납입일 기준으로 계산
# 연최고 수익률: 구한 일별 수익률 중 max
# 연최저 수익률: 구한 일별 수익률 중 min

def get_mdd(x):
    #MDD(Maximum Draw-Down)
    #:return: (peak_upper, peak_lower, mdd_rate)

    arr_v = np.array(x)
    peak_lower = np.argmax(np.maximum.accumulate(arr_v) - arr_v)
    peak_upper = np.argmax(arr_v[:peak_lower])
    return peak_upper, peak_lower, (arr_v[peak_lower] - arr_v[peak_upper]) / arr_v[peak_upper]

mdd = get_mdd(df['value'])
print(mdd)