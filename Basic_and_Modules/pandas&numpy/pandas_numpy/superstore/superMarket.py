# -*- coding: utf-8 -*-
"""
Created on Tue Aug 11 17:52:17 2020

@author: rmileng
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

os.chdir(r'D:\LYS\python_learning\exercise\pandas_numpy\superstore')
data = pd.read_csv('superstore_dataset2011-2015.csv',encoding='unicode_escape')
data.head(5)
data.info()
data.describe()
data.shape

# data cleansing
data['Order Date'] = pd.to_datetime(data['Order Date'])
data = data.sort_values('Order Date',ascending=True)
data['month'] = data['Order Date'].apply(lambda date: date.month)
data['year'] = data['Order Date'].apply(lambda date: date.year)
data['price'] = data['Sales']/data['Quantity']

sales_data = data[['Order Date','Sales','Profit','year','month']]
sales_data.head()

data_sale = data.groupby('year').sum()[['Sales','Profit','Quantity']]
data_sale['Profit Rate'] = data_sale['Profit']/data_sale['Sales']
data_sale.plot(kind='bar')
rate = data_sale.pct_change()

data['yearmonth'] = data['year']*100+data['month']
data_sale = pd.pivot_table(index='month',columns='year',values=['Sales','Profit','Quantity'],data=data,aggfunc='sum')
# plot
fig, (ax11,ax12,ax13) = plt.subplots(1,3,figsize=(20,4))
data_sale.Profit.plot(ax=ax11,title='Profit')
data_sale.Sales.plot.area(ax=ax12,stacked=False,colormap='Accent_r',title='Sales')
data_sale.Quantity.plot.area(ax=ax13,colormap='RdPu',stacked=False,title='Quantity')
fig.tight_layout()
plt.show()
data_sale.Sales.pct_change(axis=1).style.background_gradient(cmap='Greens',axis =1,low=0,high=1)

data_category = pd.pivot_table(index=['Category','Sub-Category'],values=['Sales','Profit'],data=data,aggfunc='sum')
data_category.plot(kind='bar',title='by category',color=['green','pink'],ylim=(-500000,2000000))

data_customer = data.groupby('Segment').Sales.count()
data_customer.plot.pie(autopct='%0.2f%%',cmap='Reds',title='customer distribution')
data_saleC = pd.pivot_table(data,index='Segment',columns='year',values='Sales',aggfunc='sum')
data_saleC.plot.bar(cmap='Greens',ylim=(0,2500000),stacked=False)

# 
data_new = pd.pivot_table(data,values='Customer ID',index='month',columns='year',aggfunc= lambda x: x.nunique())
id1 = data.query('year==2012 & month==1')['Customer ID']
id2 = data.query('year==2011')['Customer ID']
len([i for i in id1.values if i not in id2.values])


import numpy as np
import pandas as pd
from pandas import Series, DataFrame

np.random.seed(666)

score_list = np.random.randint(25, 100, size=20)
print(score_list)
# [27 70 55 87 95 98 55 61 86 76 85 53 39 88 41 71 64 94 38 94]

#　指定多个区间
bins = [0, 59, 70, 80, 100]

score_cut = pd.cut(score_list, bins)
print(type(score_cut)) # <class 'pandas.core.arrays.categorical.Categorical'>
print(score_cut)
'''
[(0, 59], (59, 70], (0, 59], (80, 100], (80, 100], ..., (70, 80], (59, 70], (80, 100], (0, 59], (80, 100]]
Length: 20
Categories (4, interval[int64]): [(0, 59] < (59, 70] < (70, 80] < (80, 100]]
'''
print(pd.value_counts(score_cut)) # 统计每个区间人数

df = pd.DataFrame()
df['score'] = score_list
df['student'] = [pd.util.testing.rands(3) for i in range(len(score_list))]
df['Category'] = pd.cut(df.score,bins,labels=['low', 'middle', 'good', 'perfect'])

