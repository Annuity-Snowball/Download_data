from datetime import date, timedelta

start_date = date(2008, 1, 1) 
end_date = date(2008, 12, 15)    # perhaps date.now()

delta = end_date - start_date   # returns timedelta

for i in range(delta.days + 1):
    day = start_date + timedelta(days=i)
    print(day.month)
    if day.day==1:
        print(day)