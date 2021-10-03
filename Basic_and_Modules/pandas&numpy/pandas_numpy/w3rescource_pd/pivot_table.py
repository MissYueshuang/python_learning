# -*- coding: utf-8 -*-
"""
Created on Fri Aug 21 15:42:36 2020

@author: rmileng
"""
import pandas as pd
import numpy as np

data = pd.read_excel('SaleData.xlsx')

# find the total sale amount region wise, manager wise.
result = pd.pivot_table(data,index=['Region','Manager'],values='Sale_amt',aggfunc='sum')

# find the item wise unit sold.
result = pd.pivot_table(data,index='Item',values='Units',aggfunc='sum')

# count the manager wise sale and mean value of sale amount.
result = pd.pivot_table(data,index='Manager',values='Sale_amt',aggfunc=['mean','count'])

# find manager wise, salesman wise total sale and also display the sum of all sale amount at the bottom.
result = pd.pivot_table(data,index=['Manager','SalesMan'],values=['Sale_amt','Units'],aggfunc='sum',margins=True)

# find the total sale amount region wise, manager wise, sales man wise where Manager = "Douglas".
result = pd.pivot_table(data,index=['Region','Manager','SalesMan'],values='Sale_amt',aggfunc='sum')
result.query("Manager=='Douglas'")

#  find the region wise Television and Home Theater sold.
result = pd.pivot_table(data,index=['Region','Item'],values='Units')
result.query('Item == ["Television","Home Theater"]')

# find the maximum sale value of the items.
result = pd.pivot_table(data,index='Item',values='Sale_amt',aggfunc='max')

## new exercise
data = pd.read_csv('titanic.csv')
data.info()
del data['Unnamed: 15']

data.dtypes
data.shape
data.columns

# find survival rate by gender on various classes.
pd.pivot_table(data,index='sex',columns='pclass',values='survived',aggfunc='mean')

#  find survival rate by gender.
pd.pivot_table(data,index='sex',values='survived',aggfunc='mean')
data.groupby('sex')['survived'].mean()

# partition each of the passengers into four categories based on their age.
pd.cut(data.age,[0,10,30,60,80])

# count survival by gender, categories wise age of various classes.
group = pd.cut(data.age,[0,10,30,60,80])
pd.pivot_table(data,index=['sex',group],columns='pclass',values='survived',aggfunc='count')

# Add the fare as a dimension of columns and partition fare column into 2 categories based on the values present in fare columns.
fare = pd.qcut(data['fare'], 2)
age = pd.cut(data['age'], [0, 10, 30, 60, 80])
data.pivot_table('survived', index=['sex', age], columns=[fare, 'pclass'])

# calculate how many women and men were in a particular cabin class.
pd.pivot_table(data,index='sex',columns='pclass',values='survived',aggfunc='count')

#  find number of survivors and average rate grouped by gender and class.
pd.pivot_table(data,index='sex',columns='pclass',values=['fare','survived'],aggfunc=['mean','sum'])

# find number of adult male, adult female and children.
pd.pivot_table(data,index='sex',values='who',aggfunc='sum')

# check missing values of children.
data.loc[data.who=='child'].isnull().sum()

# separate the gender according to whether they traveled alone or not to get the probability of survival.
pd.pivot_table(data,index=['sex','alone'],columns='pclass',values='survived')


