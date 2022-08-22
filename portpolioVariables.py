import yfinance as yf
import pandas as pd
import numpy as np
import datetime as dt
from pandas.tseries.offsets import *

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

#2) cumulative returns (

gross_ret = ptc_ret+1 # gross return: 총 수익률
cum_ret = gross_ret.cumprod() - 1 #누적곱

print(cum_ret.head())