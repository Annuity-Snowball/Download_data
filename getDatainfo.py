from dateutil.parser import *
from dateutil.relativedelta import *
from dateutil.rrule import *
import exchange_calendars as ecal
import warnings
import time
import pandas as pd
from datetime import datetime
from datetime import timedelta
warnings.simplefilter(action='ignore', category=FutureWarning) # FutureWaring 제거

x = ecal.get_calendar("XKRX")  # 한국 증시 코드


# print(holiday)
def getPayInDateInfo(start_date, end_date, month_type):  # 납입일 계산 (월초: 0, 월말: 1)
    rtList = []
    if month_type == '0':
        a = list(rrule(MONTHLY,
                       byweekday=(MO, TU, WE, TH, FR),
                       bysetpos=1,
                       dtstart=parse(start_date),
                       until=parse(end_date)))  # 지정된 기간의 매월 마지막 평일

        for i in a:
            if not x.is_session(i):  # 개장일이 아닌 날이 있는지 check
                i = x.next_open(i)  # 직전 개장일
            rtList.append(i.strftime('%Y-%m-%d'))  # yyyy-mm-dd 형식 변환
        if rtList[0] == x.next_open(start_date).strftime('%Y-%m-%d'):
            del rtList[0]
        return rtList  # 납입 예정일 리스트 출력

    elif month_type == '1' :
        a = list(rrule(MONTHLY,
                       byweekday=(MO, TU, WE, TH, FR),
                       bysetpos=-1,
                       dtstart=parse(start_date),
                       until=parse(end_date)))  # 지정된 기간의 매월 마지막 평일

        for i in a:
            if not x.is_session(i):  # 개장일이 아닌 날이 있는지 check
                i = x.previous_open(i)  # 직전 개장일
            rtList.append(i.strftime('%Y-%m-%d'))  # yyyy-mm-dd 형식 변환
        if rtList[0] == x.next_open(start_date).strftime('%Y-%m-%d'):
            del rtList[0]
        return rtList  # 납입 예정일 리스트 출력


def getDailyDateInfo(start_date, end_date):  # 지정한 기간 사이의 모든 개장일 반환 - PDF 크롤링에만 사용 가능(이후 1년까지만 가능)
    a = x.sessions_in_range(start_date, end_date)
    rtList = []

    for i in a:
        rtList.append(i.strftime('%Y-%m-%d'))
    return rtList

def getRebalanceDateInfo(start_date, end_date, month_type, interval):  # 리밸런싱 날짜 계산 (월초 or 월말)
    rtList = []
    if x.is_session(start_date):
        rtList.append(start_date)
    else:
        rtList.append((x.next_open(start_date)).strftime('%Y-%m-%d'))
    # month_type 0: 월초, 1: 월말

    if month_type == '0':
        a = list(rrule(MONTHLY,
                       interval=interval,
                       byweekday=(MO, TU, WE, TH, FR),
                       bysetpos=1,
                       dtstart=parse(start_date),
                       until=parse(end_date)))  # 지정된 기간의 매월 첫 평일 (월초)
        for i in a:
            if not x.is_session(i):  # 개장일이 아닌 날이 있는지 check
                i = x.next_open(i)  # 직전 개장일
            if i.strftime('%Y-%m-%d') not in rtList:
                rtList.append(i.strftime('%Y-%m-%d'))  # yyyy-mm-dd 형식 변환
        return rtList  # 납입 예정일 리스트 출력

    if month_type == '1':
        a = list(rrule(MONTHLY,
                       interval=interval,
                       byweekday=(MO, TU, WE, TH, FR),
                       bysetpos=-1,
                       dtstart=parse(start_date),
                       until=parse(end_date)))  # 지정된 기간의 매월 첫 평일 (월초)

        for i in a:
            if not x.is_session(i):  # 개장일이 아닌 날이 있는지 check
                i = x.previous_open(i)  # 직전 개장일
            if i not in rtList:
                rtList.append(i.strftime('%Y-%m-%d'))  # yyyy-mm-dd 형식 변환
        return rtList  # 납입 예정일 리스트 출력


        for i in a:
            if not x.is_session(i):  # 개장일이 아닌 날이 있는지 check
                i = x.previous_open(i)  # 직전 개장일
            rtList.append(i.strftime('%Y-%m-%d'))  # yyyy-mm-dd 형식 변환
        return rtList  # 납입 예정일 리스트 출력

def getYearlyDateInfo(start_date, end_date):  # 납입일 계산 (월초: 0, 월말: 1)
    rtList = []
    a = list(rrule(YEARLY,
        byweekday=(MO, TU, WE, TH, FR),
        bysetpos=1,
        dtstart=parse(start_date),
        until=parse(end_date)))  # 지정된 기간의 매월 마지막 평일

    for i in a:
        if not x.is_session(i):  # 개장일이 아닌 날이 있는지 check
            i = x.next_open(i)  # 직전 개장일
        rtList.append(i.strftime('%Y-%m-%d'))  # yyyy-mm-dd 형식 변환
    if rtList[0] == x.next_open(start_date).strftime('%Y-%m-%d'):
        del rtList[0]
    return rtList  # 납입 예정일 리스트 출력

# print(getYearlyDateInfo('2002-09-16', '2022-09-14'))