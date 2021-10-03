# -*- coding: utf-8 -*-
"""
Created on Sat Aug 15 10:21:55 2020

@author: rmileng
"""

import pandas as pd
import numpy as np

s1 = pd.Series({'a': 100, 'b': 200, 'c': 300, 'd': 400, 'e': 800})
s2 = pd.Series([1, 3, 'python', 7.1, 9])

pd.to_numeric(s2,errors='coerce')

s = pd.Series([
    ['Red', 'Green', 'White'],
    ['Red', 'Black'],
    ['Yellow']])
s.apply(pd.Series).stack().reset_index(drop=True)

s = pd.Series(['100', '200', 'python', '300.12', '400'])
s.sort_values()
s.append(pd.Series(['600','php']))

s = pd.Series([0, 1,2,3,4,5,6,7,8,9,10])
s[s<=5]

s = pd.Series(data = [1,2,3,4,5], index = ['A', 'B', 'C','D','E'])
s[['B','A','C','D','E']]
s.mean()
s.std()

s1 = pd.Series([1,2,3,4,5])
s2 = pd.Series([2,4,6,8,10])
s1[~s1.isin(s2)]
s1[~s1.isin(s2)].append(s2[~s2.isin(s1)]).reset_index(drop=True)

s = pd.Series(np.random.randint(0,10,10))
np.percentile(s,q=[0,25,50,75,100])
s[~s.isin(s.value_counts()[:2])] = 'other'

np.argwhere(s % 5 == 0)
s.take([0,2])

# convert the first and last character of each word to upper case in each word of a given series.
s = pd.Series(['php','python','java','c#'])
s.map(lambda x: x[0].upper() + x[1:-1] + x[-1].upper())
s.map(len)         
               
s = pd.Series(np.random.randint(1,15,7))               
s.diff().diff()               
            
date_series = pd.Series(['01 Jan 2015', '10-02-2016', '20180307', '2014/05/06', '2016-04-12', '2019-04-06T11:20'])               
date_series = pd.to_datetime(date_series)              
date_series.apply(lambda x: parse(x))          
               
from dateutil.parser import parse               
date_series = pd.Series(['Jan 2015', 'Feb 2016', 'Mar 2017', 'Apr 2018', 'May 2019'])
print("Original Series:")             
date_series.apply(lambda x: parse('11 '+ x))             
               
color_series = pd.Series(['Red', 'Green', 'Orange', 'Pink', 'Yellow', 'White'])              
from collections import Counter             
idx = color_series.map(lambda x: sum([Counter(x.lower()).get(i,0) for i in list('aeiou')]) >= 2 )            
color_series[idx]              
      
s = pd.Series([1, 8, 7, 5, 6, 5, 3, 4, 7, 1])         
[i for i in s.index.tolist()[1:-1] if (s[i] > s[i+1]) & (s[i] > s[i-1])]     
       
str1 = 'abc def abcdef icd'               
s = pd.Series(list(str1))               
s.str.replace(' ',s.value_counts().index[-1])              
               
s = pd.Series(pd.date_range(start='2020-01-01',periods=52,freq='W-SUN'))               
df = s.to_frame()             
               
s1 = pd.Series(range(10))
s2 = pd.Series(list('pqrstuvwxy'))              
pd.concat((s1,s2),axis=1)               
s1.eq(s2)              
    
s = pd.Series(np.random.randint(0,100,10))           
np.argmax(s)            
np.argmin(s)

df_data = pd.DataFrame({'W':[68,75,86,80,None],'X':[78,75,None,80,86], 'Y':[84,94,89,86,86],'Z':[86,97,96,72,83]});
sr_data = pd.Series([68, 75, 86, 80, None]) 
df_data.ne(sr_data,axis=0)
