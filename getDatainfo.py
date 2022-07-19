import dateutil.rrule
from dateutil.relativedelta import *
from dateutil.parser import *
from dateutil.rrule import *

def getDateInfo(start_date, end_date, interval):
    set = rruleset()

    if(interval == "first"):
        return list(rrule(MONTHLY, byweekday=(MO,TU,WE,TH,FR), bysetpos=1, dtstart=parse(start_date), until=parse(end_date))) # 지정된 기간의 매월 첫 평일

    else:
        return list(rrule(MONTHLY, byweekday=(MO, TU, WE, TH, FR), bysetpos=-1, dtstart=parse(start_date), until=parse(end_date)))  # 지정된 기간의 매월 마지막 평일

firstDate = getDateInfo("20220102T090000", "20221215T090000", "first")
print(firstDate)
lastDate = getDateInfo("20220102T090000", "20221215T090000", "last")
print(lastDate)