from dateutil.parser import *
from dateutil.relativedelta import *
from dateutil.rrule import *
import exchange_calendars as ecal
import warnings
import time
import pandas as pd
from datetime import datetime

warnings.simplefilter(action='ignore', category=FutureWarning) # FutureWaring 제거

x = ecal.get_calendar("XKRX")  # 한국 증시 코드

holiday = ['2022-01-31', '2022-02-01', '2022-02-02', '2022-03-01', '2022-03-09', '2022-05-05', '2022-06-01', '2022-06-06', '2022-08-15',
           '2022-09-09', '2022-09-12', '2022-10-03', '2022-10-10', '2022-12-30', '2023-01-23', '2023-01-24', '2023-03-01', '2023-05-01',
           '2023-05-05', '2023-06-06', '2023-08-15', '2023-09-28', '2023-09-29', '2023-10-03', '2023-10-09', '2023-12-25', '2023-12-29',
           '2024-01-01', '2024-02-09', '2024-02-12', '2024-03-01', '2024-05-01', '2024-05-06', '2024-05-15', '2024-06-06', '2024-08-15',
           '2024-09-16', '2024-09-17', '2024-09-18', '2024-10-03', '2024-10-09', '2024-12-25', '2024-12-31', '2025-01-01', '2025-01-28',
           '2025-01-29', '2025-01-30', '2025-03-03', '2025-05-01', '2025-05-05', '2025-05-06', '2025-06-06', '2025-08-15', '2025-10-03',
           '2025-10-06', '2025-10-07', '2025-10-08', '2025-10-09', '2025-12-25', '2026-01-01', '2026-02-16', '2026-02-17', '2026-02-18',
           '2026-03-02', '2026-05-01', '2026-05-05', '2026-08-17']

for i in holiday:
    i = datetime.strptime(i, '%Y-%m-%d')

def getPayInDateInfo(start_date, end_date, interval):  # 납입일 계산 (월초 or 월말)
    rtList = []
    if interval == "first":
        a = list(rrule(MONTHLY,
                       byweekday=(MO, TU, WE, TH, FR),
                       bysetpos=1,
                       dtstart=parse(start_date),
                       until=parse(end_date)))  # 지정된 기간의 매월 마지막 평일

        for i in a:
            if not x.is_session(i):  # 개장일이 아닌 날이 있는지 check
                i = x.previous_open(i)  # 직전 개장일
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


def getDailyDateInfo(start_date, end_date):  # 지정한 기간 사이의 모든 개장일 반환 - PDF 크롤링에만 사용 가능(이후 1년까지만 가능)
    a = x.sessions_in_range(start_date, end_date,)
    rtList = []

    for i in a:
        rtList.append(i.strftime('%Y-%m-%d'))

    return rtList

def getRebalanceDateInfo(start_date, end_date, interval):  # 리밸런싱 날짜 계산 (월초 or 월말)
    rtList = []
    # Interval -> 1: 3개월, 2: 6개월, 3: 12개월, 4: 24개월
    if interval == 1:
        a = list(rrule(MONTHLY,
                       interval=3,
                       byweekday=(MO, TU, WE, TH, FR),
                       bysetpos=1,
                       dtstart=parse(start_date),
                       until=parse(end_date)))  # 지정된 기간의 매월 첫 평일 (월초)
        for i in a:
            if not x.is_session(i):  # 개장일이 아닌 날이 있는지 check
                i = x.next_open(i)  # 다음 개장일
            rtList.append(i.strftime('%Y-%m-%d'))  # yyyy-mm-dd 형식 변환
        return rtList  # 납입 예정일 리스트 출력

    elif interval == 2:
        a = list(rrule(MONTHLY,
                       interval=6,
                       byweekday=(MO, TU, WE, TH, FR),
                       bysetpos=1,
                       dtstart=parse(start_date),
                       until=parse(end_date)))  # 지정된 기간의 매월 마지막 평일

        for i in a:
            if not x.is_session(i):  # 개장일이 아닌 날이 있는지 check
                i = x.previous_open(i)  # 직전 개장일
            rtList.append(i.strftime('%Y-%m-%d'))  # yyyy-mm-dd 형식 변환
        return rtList  # 납입 예정일 리스트 출력

    elif interval == 3:
        a = list(rrule(YEARLY,
                       byweekday=(MO, TU, WE, TH, FR),
                       bysetpos=1,
                       dtstart=parse(start_date),
                       until=parse(end_date)))  # 지정된 기간의 매월 마지막 평일

        for i in a:
            if not x.is_session(i):  # 개장일이 아닌 날이 있는지 check
                i = x.previous_open(i)  # 직전 개장일
            rtList.append(i.strftime('%Y-%m-%d'))  # yyyy-mm-dd 형식 변환
        return rtList  # 납입 예정일 리스트 출력

<<<<<<< HEAD
=======

>>>>>>> 7a26a8509a6cdfe02d69383bbaa64b096b14d733
