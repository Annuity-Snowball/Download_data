import yfinance as yf
import pandas as pd
import numpy as np
import datetime as dt
from pandas.tseries.offsets import *

# 일별 수익률: (오늘종가 - 어제 종가) / (어제 종가) -1

p_apple = yf.download('AAPL', start='2019-01-01')
p_google = yf.download('GOOGL', start='2019-01-01')

# Merge the tow tables above (표 병합)
p_apple = p_apple[['Adj Close']].rename(columns={'Adj Close': 'Close_Apple'})
p_google = p_google[['Adj Close']].rename(columns={'Adj Close': 'Close_Google'})

price = pd.concat([p_apple, p_google], axis=1)

start_date = price['Date'].astype(str).iloc[0]
end_date = price['Date'].astype(str).iloc[-1]

date_all = pd.date_range(start_date, end_date, freq='D').to_frame().rename(columns={0: 'Date'}).reset_index(drop=True)

# Merge with price data (데이터 병합)
price_all = pd.merge(date_all, price, how='left')
price_all = price_all.fillna(method='ffill')

#Generate day of week variables (요일 이름 변수 생성)
price_all['Day_Name'] = price_all['Date'].dt.day_name()

#Get Monday prices (월요일 가격만 뽑아내기)
price_mon = price_all[price_all['Day_Name']=='Monday']

# Set index and remove the Day Name columns (index 설정 및 Day_Name column 삭제)
price_mon = price_mon.set_index(['Date']).drop(['Day_Name'], axis=1)

# Monday close-to-Monday close weekly returns (월요일 종가-월요일 종가 주간 수익률)
week_mon_ret = price_mon.pct_change(1).dropna()

# Get Wednesday prices (수요일 가격만 뽑아내기)
price_wed = price_all[price_all['Day_Name'] == 'Wednesday']

# Set index and remove the Day Name columns (index 설정 및 Day_Name column 삭제)
price_wed = price_wed.set_index(['Date']).drop(['Day_Name'], axis=1)

# Wednesday close-to-Wednesday close weekly returns (수요일 종가-수요일 종가 주간 수익률)
week_wed_ret = price_wed.pct_change(1).dropna()

#Generate end of month data (월말 날짜 생성)
month_end = pd.date_range(start_date, end_date, freq='M')

#Get only end of month prices (월말 가격 데이터 생성)
price_month = price_all[price_all['Date'].isin(month_end)].reset_index(drop=True)

# Set index and remove the Day Name columns (index 설정 및 Day_Name column 삭제)
price_month = price_month.set_index(['Date']).drop(['Day_Name'], axis=1)

# Monthly returns (월 수익률)
month_ret = price_month.pct_change(1).dropna()