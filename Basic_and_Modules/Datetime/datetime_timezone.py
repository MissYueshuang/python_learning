# -*- coding: utf-8 -*-
"""
Created on Wed Jul  8 17:21:39 2020

@author: rmileng
"""
import re
from datetime import datetime, timezone, timedelta

def to_timestamp(dt_str, tz_str):
    dt = datetime.strptime(dt_str,'%Y-%m-%d %H:%M:%S')
    res = re.match(r'UTC([+-]\d+):00',tz_str).group(1)
    if res[0] == '+':
        h = int(res[1:])
    else:
        h = int(res[1:]) * (-1)
    tz_utc = timezone(timedelta(hours=h))
    dt = dt.replace(tzinfo=tz_utc)
    return dt.timestamp()
    
t1 = to_timestamp('2015-6-1 08:10:30', 'UTC+7:00')
assert t1 == 1433121030.0, t1

t2 = to_timestamp('2015-5-31 16:10:30', 'UTC-09:00')
assert t2 == 1433121030.0, t2

print('ok')

#dt_str = '2015-6-1 08:10:30'
# tz_str = 'UTC-09:00'
