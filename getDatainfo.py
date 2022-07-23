import dateutil.rrule
from dateutil.relativedelta import *
from dateutil.parser import *
from dateutil.rrule import *

def getDateInfo(start_date, end_date, interval):
    set = rruleset()

    if(interval == "first"):
        lst =  list(rrule(MONTHLY, byweekday=(MO,TU,WE,TH,FR), bysetpos=1, dtstart=parse(start_date), until=parse(end_date))) # 지정된 기간의 매월 첫 평일

    else:
        lst =  list(rrule(MONTHLY, byweekday=(MO, TU, WE, TH, FR), bysetpos=-1, dtstart=parse(start_date), until=parse(end_date)))  # 지정된 기간의 매월 마지막 평일
    rtList = []
    for i in lst:
        rtList.append(i.strftime('%Y-%m-%d')) 

    print(rtList)

firstDate = getDateInfo("20220102", "20221215", "first")
# print(firstDate[0].strftime('%Y-%m-%d'))
