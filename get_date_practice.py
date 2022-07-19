from datetime import date, timedelta
from dateutil.relativedelta import relativedelta
start_date = date(2008, 1, 1) 
end_date = date(2008, 12, 15)    # perhaps date.now()

delta = end_date - start_date   # returns timedelta

for i in range(delta.days + 1):
    day = start_date + timedelta(days=i)
    if day.day==1:
        print(day)