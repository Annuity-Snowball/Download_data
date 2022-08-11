from dateutil.parser import *
from dateutil.relativedelta import *
from dateutil.rrule import *
import exchange_calendars as ecal
import time
import pandas as pd
from datetime import datetime

x = ecal.get_calendar("XKRX")  # 한국 증시 코드


def getPayInDateInfo(start_date, end_date, interval):  # 납입일 계산 (월초 or 월말)
    rtList = []
    if interval == "first":
        a = list(rrule(MONTHLY, byweekday=(MO, TU, WE, TH, FR),
                       bysetpos=1,
                       dtstart=parse(start_date),
                       until=parse(end_date)))  # 지정된 기간의 매월 첫 평일 (월초)
        for i in a:
            if not x.is_session(i):  # 개장일이 아닌 날이 있는지 check
                i = x.next_open(i)  # 다음 개장일
            rtList.append(i.strftime('%Y-%m-%d'))  # yyyy-mm-dd 형식 변환
        return rtList  # 납입 예정일 리스트 출력

    else:
        a = list(rrule(MONTHLY,
                       byweekday=(MO, TU, WE, TH, FR),
                       bysetpos=-1,
                       dtstart=parse(start_date),
                       until=parse(end_date)))  # 지정된 기간의 매월 마지막 평일

        for i in a:
            if not x.is_session(i):  # 개장일이 아닌 날이 있는지 check
                i = x.previous_open(i)  # 직전 개장일
            rtList.append(i.strftime('%Y-%m-%d'))  # yyyy-mm-dd 형식 변환
        return rtList  # 납입 예정일 리스트 출력


def getDailyDateInfo(start_date, end_date):  # 지정한 기간 사이의 모든 개장일 반환
    a = x.sessions_in_range(start_date, end_date,)
    rtList = []

    for i in a:
        rtList.append(i.strftime('%Y-%m-%d'))

    return rtList

print(getDailyDateInfo("2022-01-01", "2022-08-11"))


# data = pd.read_csv("ad.csv", sep=",")
# period = []

# for r in data['date']:
#     period.append(getDailyDateInfo(r, datetime.today().strftime('%Y-%m-%d')))

