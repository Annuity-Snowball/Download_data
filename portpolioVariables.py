import yfinance as yf
import pandas as pd
import numpy as np
import datetime as dt
from pandas.tseries.offsets import *

# 일별 수익률: (오늘종가 - 어제 종가) / (어제 종가) -1 의 가중평균

p_apple = yf.download('AAPL', start='2019-01-01')
p_google = yf.download('GOOGL', start='2019-01-01')
#Test portpolio variables from stock data

#Download price data from yfinance (가격 데이터 다운로드)
p_apple = yf.download('AAPL',start = '2019-01-01')
p_google = yf.download('GOOGL',start = '2019-01-01')

#Extract Adj close price
p_apple = p_apple[['Adj Close']].rename(columns = {'Adj Close':'Close_Apple'})
p_google = p_google[['Adj Close']].rename(columns = {'Adj Close':'Close_Google'})

price = pd.concat([p_apple, p_google], axis=1)

#1) daily returns = (today price - previous price) / (previous price) - 1
ptc_ret = price.pct_change(1).dropna() # dropna(): Eliminate NaN Value
ptc_ret = ptc_ret.rename(columns={'Close_Apple':'Ret_Apple', 'Close_Google': 'Ret_Google'})
print(ptc_ret.head())

#2) cumulative returns do {(current return+1)*(previous return+1) -1} until today -> 누적곱
gross_ret = ptc_ret+1 # gross return: 총 수익률
cum_ret = gross_ret.cumprod() - 1 #누적곱

print(cum_ret.head())

#포트폴리오 -> 가중평균으로 구하기 ex) 상품a $100, 상품b $200 -> 1/3, 2/3 가중치로 계산하여 평균 구하기

# MDD : 특정 기간동안 발생한 최대 낙폭 = (기간동안의 최저점 - 기간동안의 최고점) / 기간동안의 최고점 -> 종목별로 구해서 가중평균내기
# 승률 : 납입일 기준으로 계산
# 연최고 수익률: 구한 일별 수익률 중 max
# 연최저 수익률: 구한 일별 수익률 중 min
