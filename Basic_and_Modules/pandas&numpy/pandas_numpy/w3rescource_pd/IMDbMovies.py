# -*- coding: utf-8 -*-
"""
Created on Thu Nov 26 21:44:12 2020

IMDb Movies Data Analysis

@author: rmileng
"""
import numpy as np
import pandas as pd
pd.options.display.max_columns=4
pd.options.display.max_rows=5

diamonds = pd.read_csv('https://raw.githubusercontent.com/mwaskom/seaborn-data/master/diamonds.csv')

# 6 summarize only 'object' columns
diamonds.select_dtypes(include='object').describe()

# remove the second column
diamonds.drop(axis=1,columns=1)

# convert a python list to pandas series
l = [1,2,3,4]
pd.Series(l)

#  read only a subset of 3 rows
result = pd.read_csv('https://raw.githubusercontent.com/mwaskom/seaborn-data/master/diamonds.csv', nrows=3)

# iterate through diamonds DataFrame
for idx,row in diamonds.iterrows():
    print(idx,row)
    
# drop all non-numeric columns
idx = list(diamonds.columns[diamonds.dtypes=='float64'])
diamonds[idx]

# calculate the mean of each numeric column
diamonds.select_dtypes(include=np.number)

# mean of each row 
diamonds.mean(axis=1) # automatically ignore non-numeric columns

# the mean of price for each cut of diamonds
diamonds.groupby('cut')['price'].mean()

# calculate count, minimum, maximum price for each cut of diamonds
diamonds.groupby('cut')['price'].agg(['count','min','max'])

# 30. create a side-by-side bar plot of the diamonds 
diamonds.groupby('cut').mean().plot(kind='bar')

# 31 count how many times each value in cut series of diamonds
diamonds.cut.value_counts()

# 32  display percentages of each value of cut series occurs
diamonds.cut.value_counts()/diamonds.shape[0]
diamonds.cut.value_counts(normalize=True)

#  33 unique values  in cut series
diamonds.cut.unique()
diamonds.cut.drop_duplicates()

# 34count the number of unique values in cut series     
diamonds.cut.nunique()

# compute a cross-tabulation of two Series
pd.crosstab(diamonds.cut, diamonds.price)

#  calculate various summary statistics of cut series of diamonds
diamonds.carat.describe()

# 37. create a histogram of the 'carat' Series
diamonds.carat.plot(kind='hist')

# 38 create a bar plot of the 'value_counts' for the 'cut' series
diamonds.cut.value_counts().plot(kind='bar')

# 39  create a DataFrame of booleans (True if missing, False if not missing) from diamonds DataFrame. 
diamonds.isnull()

# 40.  count the number of missing values in each Series of diamonds
df = diamonds.isnull().sum(axis=0)

# 41. check the number of rows and columns and drop those row if 'any' values are missing in a row of diamonds
diamonds[diamonds.notnull().any(axis=1)]
diamonds.dropna(how='any')

# 42. drop a row if any or all values in a row are missing of diamonds DataFrame on two specific columns.
diamonds.dropna(how='any',subset=['carat','color'])

diamonds.loc[0:2, 'color':'price']
diamonds.iloc[0:2, 0:2]

diamonds.info(memory_usage='deep')

# 43. get randomly sample rows
diamonds.sample(5)

# get sample 75% of the diamonds DataFrame's rows without replacement and store the remaining 25% of the rows in another DataFrame.
df = diamonds.sample(frac=0.75,replace=False)
df2 = diamonds.drop(index=df.index)

#  count the duplicate rows
diamonds[diamonds.duplicated()].shape[0]
diamonds.duplicated().sum()

#  detect duplicate color. 
diamonds.clarity.duplicated().sum()

