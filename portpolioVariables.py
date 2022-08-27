import datetime
import yfinance as yf
import pandas as pd
import numpy as np
import datetime as dt
from pandas.tseries.offsets import *
from pandas_datareader import data as pdr
import matplotlib.pyplot as plt

# 수익률: ((당일 가치) -(원금) + (현금)) / (원금) -> return column
# MDD: 특정 기간동안 발생한 최대 낙폭 = (기간동안의 최저점 - 기간동안의 최고점) / 기간동안의 최고점
# 승률: 리밸런싱일 기준으로 계산
# 연최고 수익률: return column 중 max value
# 연최저 수익률: return column 중 min value

values= {'2021-01-01': [1000000.0, 949528.0],'2021-01-10': [1000000.0, 512878.0], '2021-01-15': [1000000.0, 1112878.0], '2021-02-01': [1500000.0, 1646600.0], '2021-02-15': [1500000.0, 1533469.0],
          '2021-03-01': [2000000.0, 2203818.0], '2021-03-15': [2000000.0, 1974316.0], '2021-04-01': [2500000.0, 2101941.0], '2021-04-15': [2500000.0, 2464465.0],
          '2021-05-01': [3000000.0, 2450307.0], '2021-05-15': [3000000.0, 3001719.0], '2021-06-01': [3500000.0, 3626080.0]}


df = pd.DataFrame.from_dict(values, orient='index', columns=['seed', 'value'])
df['seed_val_ratio'] = df['value']/df['seed']
df['return'] = (df['value'] - df['seed']) / df['seed']

# gross_ret = df['return']+1
# df['cum_ret'] = gross_ret.cumprod() - 1

print(df)

def get_mdd(x):
    #전범위
    #MDD(Maximum Draw-Down): 기간 내 최대 낙폭
    #:return: (peak_upper, peak_lower, mdd_rate)

    arr_v = np.array(x)
    peak_lower = np.argmax(np.maximum.accumulate(arr_v) - arr_v)
    peak_upper = np.argmax(arr_v[:peak_lower])
    return peak_upper, peak_lower, (arr_v[peak_lower] - arr_v[peak_upper]) / arr_v[peak_upper] # (기간 최저) - (기간 최고) / (기간 최고)
# mdd = get_mdd(df['seed_val_ratio'])
# print(mdd)

window = 12 # 기간
max_in_seedvalratio = df['seed_val_ratio'].rolling(window, min_periods=1).max() # 기간동안의 최댓값 저장
dd = ((df['seed_val_ratio']) / max_in_seedvalratio - 1.0) * 100 # DD: 현재값/최댓값(기간) - 1
mdd = dd.rolling(window, min_periods=1).min() # 기간 내 DD중 최솟값

# print()
# print("DD")
# print(dd)
# print()
# print("MDD")
# print(mdd)

# DD 그래프
# plt.plot(dd.index, dd, color = "brown", label = "DD")
# plt.ylabel("Drop Rate(%)")
# plt.legend()
# plt.show()

plt.subplot(311)
plt.plot(df.index, df['seed_val_ratio'], color = "green",  label = 'SV_ratio')
plt.ylabel("Index")
plt.legend()

plt.subplot(312)
plt.plot(dd.index, dd, color = "brown",  label = "DD")
plt.ylabel("Drop Rate(%)")
plt.legend()

plt.subplot(313)
plt.plot(mdd.index, mdd, color = "red",  label = "MDD")
plt.ylabel("Drop Rate(%)")
plt.legend()

plt.show()
print("기간 최고 수익률: ", df['return'].max())
print("기간 최저 수익률: ", df['return'].min())