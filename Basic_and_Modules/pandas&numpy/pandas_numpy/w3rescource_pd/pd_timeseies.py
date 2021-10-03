# -*- coding: utf-8 -*-
"""
Created on Wed Aug 19 15:07:27 2020

@author: rmileng
"""
import numpy as np
import pandas as pd
from datetime import datetime
from dateutil import parser

'''
a) Datetime object for Jan 15 2012.
b) Specific date and time of 9:20 pm.
c) Local date and time.
d) A date without time.
e) Current date.
f) Time from a datetime.
g) Current local time.
'''
pd.Timestamp('2012-01-15')
datetime(2012,1,15)

pd.Timestamp('2012-01-15 09:20 pm')
datetime(2012,1,15,21,20)

pd.Timestamp('now')
datetime.now().date()
datetime.now().time()

# a time adds in the current local date using timestamp.
pd.Timestamp('11:30')

# create a date from a given year, month, day and another date from a given string formats. 
datetime(2020,8,25)
parser.parse("1st of January, 2021")

# print the day after and before a specified date.
dt = pd.Timestamp(2012,10,30)
dt + pd.Timedelta('1d')
dt - pd.Timedelta('1d') # (days=1)
(pd.Timestamp(2012,10,30) - pd.Timestamp(2012,9,26)).days

##create a time-series with two index labels and random values.
time_series = pd.DataFrame(np.random.randn(2), columns = ['num'], index=pd.DatetimeIndex(['2011-9-1','2011-9-2']))
type(time_series.index)

## create a time-series from a given list of dates as strings.
dates = ['2014-08-01','2014-08-02','2014-08-03','2014-08-04']
time_series= pd.Series(np.random.randn(4),dates)
type(time_series.index)

## select the dates of same year and select the dates between certain dates.
index = pd.DatetimeIndex(['2011-09-02', '2012-08-04',
                          '2015-09-03', '2010-08-04',
                          '2015-03-03', '2011-08-04',
                          '2015-04-03', '2012-08-04'])
s_dates = pd.Series([0, 1, 2, 3, 4, 5, 6, 7], index=index)
s_dates[s_dates.index.year == 2015] #Dates of same year
s_dates['2015']

s_dates[(s_dates.index > datetime(2012,1,1)) & (s_dates.index < datetime(2012,12,31))]
s_dates['2012-01-01':'2012-12-31']

# create a date range using a startpoint date and a number of periods.
pd.date_range('2020-01-01',periods=30)

## create a whole month of dates in daily frequencies. Also find the maximum, minimum timestamp and indexs
ts = pd.Series(pd.date_range('2020-12-01',periods=31))
ts.max()
ts.min()
ts.idxmax()

## three months frequency.
pd.Series(pd.date_range('2020-12-01',periods=3,freq='3M'))

##  create a sequence of durations increasing by an hour.
pd.Series(pd.date_range('2020-1-1 12:00:00',periods=60,freq='T'))

## convert year and day of year into a single datetime column of a dataframe.
data = {\
"year": [2002, 2003, 2015, 2018],
"day_of_the_year": [250, 365, 1, 140]
}
data = pd.DataFrame(data)
data['combined'] = data.year*1000+data.day_of_the_year
data['date'] = data.combined.apply(lambda x: pd.to_datetime(x,format='%Y%j'))

## create a series of Timestamps using specified columns.
df = pd.DataFrame({'year': [2018, 2019, 2020],
                   'month': [2, 3, 4],
                   'day': [4, 5, 6],
                   'hour': [2, 3, 4]})
pd.to_datetime(df)
pd.to_datetime(df[['year','month','day']])

## check if a day is a business day (weekday) or not.
def is_business_day(date):
    return bool(len(pd.bdate_range(date,date)))
is_business_day('2020-08-22')

## get a time series with the last working days of each month of a specific year. 
pd.date_range('2020-1-1',freq=12,freq='BM')

## create a time series combining hour and minute.
pd.timedelta_range(0, periods=30, freq="1H20T")

## convert unix/epoch time to a regular time stamp in UTC. Also convert the said timestamp in to a given time zone.
epoch_t = 1621132355
time_stamp = pd.to_datetime(epoch_t,unit='s')
time_stamp.tz_localize('UTC').tz_convert('US/Pacific')

# remove the time zone information from a Time series data.
date1 = pd.Timestamp('2019-01-01', tz='Europe/Berlin')
date1.tz_localize(None)













