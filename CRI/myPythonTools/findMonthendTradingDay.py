# -*- coding: utf-8 -*-
"""
Created on Wed Mar 11 16:16:59 2020

@author: rmileng
"""
import calendar
import datetime

def findMonthendTradingDay(inputDate):
    Year = int(str(inputDate)[:4])
    Month = int(str(inputDate)[4:6])
    rang,date = calendar.monthrange(Year,Month)
    weekday = datetime.date(Year,Month,date).weekday()
    
    if weekday == 5: # saturday
        lastBizDay = Year*10000 + Month*100 + date - 1
    elif weekday == 6: # sunday
        lastBizDay = Year*10000 + Month*100 + date - 2
    else:
        lastBizDay = Year*10000 + Month*100 + date
        
    return lastBizDay