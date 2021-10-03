# -*- coding: utf-8 -*-
"""
Created on Tue Jan  7 14:33:32 2020

@author: rmileng
"""
from pandas import DataFrame, read_csv

import matplotlib.pyplot as plt
import pandas as pd #this is how I usually import pandas
import sys #only needed to determine Python version number
import matplotlib #only needed to determine Matplotlib version number
import numpy.random as np

print('Python version ' + sys.version)
print('Pandas version ' + pd.__version__)
print('Matplotlib version ' + matplotlib.__version__)

names = ['Bob','Jessica','Mary','John','Mel']
births = [968, 155, 77, 578, 973]

# To merge these two lists together we will use the zip function.
BabyDataSet = list(zip(names,births))
# export 
df = pd.DataFrame(data = BabyDataSet, columns=['Names', 'Births'])
df.to_csv('D:/LYS/python learning/births1880.csv',index=False,header=False)

Location = r'D:/LYS/python learning/births1880.csv'
df2 = pd.read_csv(Location)

import os
os.remove(Location)
Sorted = df.sort_values(['Births'], ascending=False)

# Create graph
df['Births'].plot()
MaxValue = df['Births'].max()
MaxName = df['Names'][df['Births'] == df['Births'].max()].values
Text = str(MaxValue) + " - " + MaxName
# Add text to graph
plt.annotate(Text, xy=(1, MaxValue), xytext=(8, 0), 
                 xycoords=('axes fraction', 'data'), textcoords='offset points')
print("The most popular name")
df[df['Births'] == df['Births'].max()]


names = ['Bob','Jessica','Mary','John','Mel']
random.seed(500) # so we will always have identical results. Otherwise, it changes everytime
random_names = [names[random.randint(low=0,high=len(names))] for i in range(1000)]
random_names[:10] # Print first 10 records
# The number of births per name for the year 1880
births = [random.randint(low=0,high=1000) for i in range(1000)]
births[:10]
BabyDataSet = list(zip(random_names,births))
BabyDataSet[:10]
df.info
df['Names'].unique()
for x in df['Names'].unique():
    print(x)
print(df['Names'].describe())
name = df.groupby('Names')
df = name.sum()
# Analyze Data
Sorted = df.sort_values(['Births'], ascending=False)
Sorted.head(1)
# or
df['Births'].max()
# Create graph
df['Births'].plot.bar()
print("The most popular name")
df.sort_values(['Births'], ascending=False)

np.seed(111)
# Function to generate test data
def CreateDataSet(Number=1):
    
    Output = []
    
    for i in range(Number):
        
        # Create a weekly (mondays) date range
        rng = pd.date_range(start='1/1/2009', end='12/31/2012', freq='W-MON')

        # Create random data
        data = np.randint(low=25,high=1000,size=len(rng))
        
        # Status pool
        status = [1,2,3]
        
        # Make a random list of statuses
        random_status = [status[np.randint(low=0,high=len(status))] for i in range(len(rng))]
        
        # State pool
        states = ['GA','FL','fl','NY','NJ','TX']
        
        # Make a random list of states 
        random_states = [states[np.randint(low=0,high=len(states))] for i in range(len(rng))]
    
        Output.extend(zip(random_states, random_status, data, rng))
        
    return Output

######
dataset = CreateDataSet(4)
df = pd.DataFrame(data=dataset, columns=['State','Status','CustomerCount','StatusDate'])
df.info()
# Clean State Column, convert to upper case
df['State'] = df.State.apply(lambda x: x.upper())
df['State'].unique()

myList = [10, 25, 17, 9, 30, -5]
# Double the value of each element
myList2 = map(lambda n : n*2, myList)
print(myList2)

# Only grab where Status == 1
mask = df['Status'] == 1
df = df[mask]
# or
df[df['Status']==1]

# Convert NJ to NY
mask = df.State == 'NJ'
df['State'][mask] = 'NY'
df['CustomerCount'].plot(figsize=(15,5))
sortdf = df[df['State']=='NY'].sort_index(axis=0)
Daily = df.reset_index().groupby(['State','StatusDate']).sum()
Daily.head()
Daily.index.levels[1]
Daily['CustomerCount'].loc['FL'].plot()


# Calculate Outliers
StateYearMonth = Daily.groupby([Daily.index.get_level_values(0), Daily.index.get_level_values(1).year, Daily.index.get_level_values(1).month]) # group by index: state. year, month
Daily['Lower'] = StateYearMonth['CustomerCount'].transform( lambda x: x.quantile(q=.25) - (1.5*x.quantile(q=.75)-x.quantile(q=.25)) )
Daily['Upper'] = StateYearMonth['CustomerCount'].transform( lambda x: x.quantile(q=.75) + (1.5*x.quantile(q=.75)-x.quantile(q=.25)) )
Daily['Outlier'] = (Daily['CustomerCount'] < Daily['Lower']) | (Daily['CustomerCount'] > Daily['Upper']) 

# Remove Outliers
Daily = Daily[Daily['Outlier'] == False]
Daily.head()
# Get the max customer count by Date
ALL = pd.DataFrame(Daily['CustomerCount'].groupby(Daily.index.get_level_values(1)).sum())
ALL.columns = ['CustomerCount'] # rename column
# Group by Year and Month
YearMonth = ALL.groupby([ALL.index.get_level_values(0).year, ALL.index.get_level_values(0).month])
# or
YearMonth = ALL.groupby([lambda x: x.year, lambda x: x.month])
# What is the max customer count per Year and Month
ALL['MAX'] = YearMonth['CustomerCount'].transform(lambda x: x.max())
ALL.head()
NEWALL = YearMonth.CustomerCount.apply(lambda x: x.max())


# Create the BHAG dataframe
data = [1000,2000,3000]
idx = pd.date_range(start='2011-12-31',end='2013-12-31',freq='Y')
BHAG = pd.DataFrame(data=data,columns=['BHAG'],index=idx)
# Combine the BHAG and the ALL data set 
combined = pd.concat([ALL,BHAG], axis=0)
combined = combined.sort_index(axis=0)
combined.tail()

fig, axes = plt.subplots(figsize=(12, 7))
combined['BHAG'].fillna(method='pad').plot(color='green', label='BHAG')
combined['MAX'].plot(color='blue', label='All Markets')
plt.legend(loc='best');

# Group by Year and then get the max value per year
Year = combined.groupby(lambda x: x.year).max()
# Add a column representing the percent change per year
Year['YR_PCT_Change'] = Year['MAX'].pct_change(periods=1)
# To get next year's end customer count we will assume our current growth rate remains constant
(1+Year.loc[2012,'YR_PCT_Change'])*Year.loc[2012,'MAX']

# present data
ALL['MAX'].plot(figsize=(10, 5));
plt.title('ALL Markets')
# Last four Graphs
fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(20, 10))
fig.subplots_adjust(hspace=1.0) ## Create space between plots

Daily.loc['FL']['CustomerCount']['2012':].fillna(method='pad').plot(ax=axes[0,0])
Daily.loc['GA']['CustomerCount']['2012':].fillna(method='pad').plot(ax=axes[0,1]) 
Daily.loc['TX']['CustomerCount']['2012':].fillna(method='pad').plot(ax=axes[1,0]) 
Daily.loc['NY']['CustomerCount']['2012':].fillna(method='pad').plot(ax=axes[1,1]) 

# Add titles
axes[0,0].set_title('Florida')
axes[0,1].set_title('Georgia')
axes[1,0].set_title('Texas')
axes[1,1].set_title('North East')







































