# -*- coding: utf-8 -*-
"""
Created on Fri Mar 27 13:49:48 2020

知识点： datetime处理，subplot

@author: rmileng
"""
import pandas as pd
import matplotlib.pyplot as plt
import datetime
from dateutil.parser import parse
import numpy as np

path = r'D:\LYS\python_learning\exercise\pandas_numpy\phone_call'
data = pd.read_csv(path+r'\Recordings.csv')

def get_weekdays(day): # day = '2020-02-13'
    date = int(parse(day).strftime('%Y%m%d'))
    datelist = np.arange(date-6,date+6)
    weekdaylsit = [parse(str(d)).weekday() for d in datelist]
    start_point = weekdaylsit.index(0)
    end_point = weekdaylsit.index(6,start_point)
    weekdayList = datelist[start_point:end_point+1]
    weekdayList = [datetime.datetime.strptime(str(d),'%Y%m%d').date().strftime('%Y-%m-%d') for d in weekdayList]
    return weekdayList

# datetime treatment
#data['am/pm'] = [date.split(' ')[5] for date in data.iloc[:,0]]
data['datetime'] = [date.split(' ')[2]+' '+date.split(',')[0] + ' ' + date.split(' ')[4]+' '+date.split(' ')[5] for date in data.iloc[:,0]]
#data['date'] = [parse(date).strftime('%Y-%m-%d %H') for date in data['datetime']]
data['date'] = [parse(date).strftime('%Y-%m-%d') for date in data['datetime']]
data['hour'] = [parse(date).strftime('%H') for date in data['datetime']]
data.hour = data.hour.astype(int)
date = data['date'].unique()

'''
I'd like a histogram created for number of calls per hour of the day. 
For example, a bar chart with the length of the bars being the number of calls and the other axis being the hour 
of the day in which the date/time occurred. So, there would be 24 bars here.
'''
date1 = date[0] # start test from first day

data_temp = data[data['date']== date1][['hour','Length']]
grouped = data_temp.groupby('hour',as_index=False).count()
dailydata = pd.DataFrame(np.arange(0,24).reshape(24,1),columns=['hour'])
plotdata = dailydata.merge(grouped,how='outer')
plotdata.hour = plotdata.hour.astype(str)+':00'

## plot
# fig, ((ax11),(ax21)) = plt.subplots(2,4)
fig = plt.figure(figsize = (20,10))

#fig.set_size_inches(20,10)
fig.subplots_adjust(top=0.9,wspace= 0.25, hspace = 0.25) # w: 子图水平间距，h:子图垂直间距

# subplot 1
ax11 = plt.subplot2grid((2,4),(0,1),colspan=2,rowspan=1)
ax11.bar(plotdata.hour,plotdata.Length)
ax11.set_xlim((0,23))
ax11.set_ylim((0,4))
xtick = plotdata.hour.tolist()
ax11.set_xticks(xtick)
ax11.set_xticklabels(xtick,rotation=45)
ax11.set_xlabel('ocurr hour')
ax11.set_ylabel('count call')
ax11.set_title('%s call distribution' % date1)

# subplot2
weekdayList = get_weekdays(date1)
data_temp = data[data['date'].isin(weekdayList)][['date','hour','Length']]
grouped = data_temp.groupby(['date','hour'],as_index=False).count()
dailydata = pd.DataFrame(list(np.arange(0,24).reshape(24,1))*7,columns=['hour'])
dailydata.insert(0,'date',np.repeat(weekdayList,24))
plotdata = dailydata.merge(grouped,how='outer')
plotdata['datetime'] = plotdata.date+" "+plotdata.hour.astype(str)+':00'

ax21 = plt.subplot2grid((2,4),(1,0),colspan=4,rowspan=1)
ax21.bar(plotdata.datetime,plotdata.Length)
ax21.set_xlim((0,168))
ax21.set_ylim((0,4))

xtick = plotdata.datetime.tolist()
tick_idx = np.arange(0,168,4)
new_label = [xtick[i] for i in tick_idx]
ax21.set_xticks(new_label)
ax21.set_xticklabels(new_label,rotation=45)
ax21.set_xlabel('ocurr hour')
ax21.set_ylabel('count call')
ax21.set_title('%s weekly call distribution' % date1)

# the end
title = 'date %s plot' % date1
fig.suptitle(title,fontsize=30, y=0.98)
# plt.tight_layout() # make the x label complete, but it will make pad parameter invalid
plt.savefig(path+r'\%s.png'%title)
plt.show()

'''
I'd also like a second histogram with calls per hour across a week. 
So, there would be 24*7=168 bars.
'''


'''
I would like to have a configuration parameter in the script which controls the minimum number of seconds that the 
call has to last in order to show up in these two histograms. The default would be 0.
'''


    
    
    
    
    
    
    
    
    
    