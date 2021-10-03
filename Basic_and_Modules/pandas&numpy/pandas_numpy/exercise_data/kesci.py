# -*- coding: utf-8 -*-
"""
Created on Wed Jul 29 17:46:14 2020

@author: rmileng
"""

import pandas as pd
import os
import datetime
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

os.chdir(r'D:\LYS\python_learning\exercise\pandas_numpy\exercise_data')

path = r'D:\LYS\python_learning\exercise\pandas_numpy\exercise_data\chipotle.tsv'

chipo = pd.read_csv(path,sep='\t')
chipo.head(10)
chipo.columns
chipo.shape[1]

grouped = chipo[['quantity','item_name']].groupby('item_name',as_index=False).agg({'quantity':'sum'})
popular_item = grouped.nlargest(5,'quantity')

chipo.item_name.nunique()
chipo['choice_description'].value_counts().head(5)
chipo.quantity.sum()

chipo.item_price = list(map(lambda x: float(x[1:-1]),chipo.item_price))
chipo['sub_total'] = round(chipo.quantity * chipo.item_price,2)
revenue = chipo['sub_total'].sum()

chipo.order_id.nunique()
#  每一单(order)对应的平均总价是多少？
chipo[['order_id','sub_total']].groupby('order_id').agg({'sub_total':'sum'}).sub_total.mean()

chipo.item_name.unique()


## filter and order
path2 = r"D:\LYS\python_learning\exercise\pandas_numpy\exercise_data\Euro2012_stats.csv"      # Euro2012_stats.csv
euro12 = pd.read_csv(path2)
euro12.Team.nunique()
euro12.shape[1]
discipline = euro12[['Team','Yellow Cards','Red Cards']]
discipline.sort_values(['Red Cards','Yellow Cards'],ascending=False)
round(discipline['Yellow Cards'].mean())
euro12[euro12.Goals>6]
# euro12[euro12.Team.isin([i for i in euro12.Team if i[0]=='G'])]
euro12[euro12.Team.str.startswith('G')]
euro12.iloc[:,:-3]
euro12.loc[euro12.Team.isin(['England','Italy','Russia']),['Team','Shooting Accuracy']]

## groupby
path3 = r'D:\LYS\python_learning\exercise\pandas_numpy\exercise_data\drinks.csv'
drinks = pd.read_csv(path3)
drinks.groupby('continent').beer_servings.mean().nlargest(5)
drinks.groupby('continent').wine_servings.describe()
drinks.groupby('continent').spirit_servings.agg(['mean','max','min'])

## apply
path4 = r'D:\LYS\python_learning\exercise\pandas_numpy\exercise_data\US_Crime_Rates_1960_2014.csv'
crime = pd.read_csv(path4)
crime.info()
crime.Year = pd.to_datetime(crime.Year,format = '%Y')
crime = crime.set_index('Year',drop=True)
del crime['Total']
# 按照Year对数据框进行分组并求和
crimes = crime.resample('10AS').sum()
population = crime['Population'].resample('10AS').max()
crimes['Population'] = population
crime.idxmax(0)

## merge
raw_data_1 = {
        'subject_id': ['1', '2', '3', '4', '5'],
        'first_name': ['Alex', 'Amy', 'Allen', 'Alice', 'Ayoung'], 
        'last_name': ['Anderson', 'Ackerman', 'Ali', 'Aoni', 'Atiches']}

raw_data_2 = {
        'subject_id': ['4', '5', '6', '7', '8'],
        'first_name': ['Billy', 'Brian', 'Bran', 'Bryce', 'Betty'], 
        'last_name': ['Bonder', 'Black', 'Balwner', 'Brice', 'Btisan']}

raw_data_3 = {
        'subject_id': ['1', '2', '3', '4', '5', '7', '8', '9', '10', '11'],
        'test_id': [51, 15, 15, 61, 16, 14, 15, 1, 61, 16]}

data1 = pd.DataFrame(raw_data_1, columns = ['subject_id', 'first_name', 'last_name'])
data2 = pd.DataFrame(raw_data_2, columns = ['subject_id', 'first_name', 'last_name'])
data3 = pd.DataFrame(raw_data_3, columns = ['subject_id','test_id'])

all_data = pd.concat([data1,data2],axis=0)
all_data_col = pd.concat([data1,data2],axis=1)
print(data3)

pd.merge(data1,data2,on='subject_id',how='outer')

# statistics
path6 = "wind.data"  # wind.data
data = pd.read_table(path6,sep='\s+',parse_dates = [[0,1,2]])

def fix_century(x):
    year = x.year-100 if x.year>1989 else x.year
    return datetime.date(year,x.month,x.day)
    
data['Yr_Mo_Dy'] = data['Yr_Mo_Dy'].apply(fix_century)

data['Yr_Mo_Dy'] = pd.to_datetime(data['Yr_Mo_Dy'])
data.set_index('Yr_Mo_Dy',inplace=True)
data.notnull().sum()
data.mean().mean()
loc_stats = data.apply(['min','max','mean','std'])
loc_stats = loc_stats.T
day_stats = data.apply(['min','max','mean','std'],axis=1)

# method 2
data['date'] = data.index

# creates a column for each value from date
data['month'] = data['date'].apply(lambda date: date.month)
data['year'] = data['date'].apply(lambda date: date.year)
data['day'] = data['date'].apply(lambda date: date.day)

# gets all value from the month 1 and assign to janyary_winds
january_winds = data.query('month == 1')
# gets the mean from january_winds, using .loc to not print the mean of month, year and day
january_winds.loc[:,'RPT':"MAL"].mean()

## visualization
path7 = 'train.csv'
titanic = pd.read_csv(path7)
titanic = titanic.set_index('PassengerId')
titanic.plot('Sex',kind='pie')

males = (titanic.Sex == 'male').sum()
females = (titanic.Sex == 'female').sum()
proportions = [males, females]

# matplot.plt
plt.title('sex proportions')
plt.pie(proportions,labels=['males','females'],colors=['blue','red'],autopct = '%1.1f%%')
plt.tight_layout()
plt.show()

# 绘制一个展示船票Fare, 与乘客年龄和性别的散点图
# my answer
titanic['sexNum'] = np.where(titanic.Sex=='male',1,0)

f,(ax11,ax21) = plt.subplots(2,1)
#f.tight_layout()
f.subplots_adjust(top=0.8)
titanic.plot('Age','Fare',kind='scatter',ax=ax11,color='b',title='Age')
titanic.plot('sexNum','Fare',kind='scatter',ax=ax21,color='r',title='Sex')
plt.show()

# template answer
lm = sns.lmplot(x='Age',y='Fare',data=titanic,hue='Sex',fit_reg=False)
lm.set(title='Fare*Age')
axes = lm.axes
axes[0,0].set_ylim(-5,)
axes[0,0].set_xlim(-5,85)
# 绘制一个展示船票价格的直方图
df = titanic.Fare.sort_values(ascending=False)
binsVal = np.arange(0,600,10)
plt.hist(df,bins=binsVal)
plt.xlabel('Fare')
plt.ylable('Freq')
plt.title('Fare payed Hist')
plt.show()

# exercise 8
raw_data = {"name": ['Bulbasaur', 'Charmander','Squirtle','Caterpie'],
            "evolution": ['Ivysaur','Charmeleon','Wartortle','Metapod'],
            "type": ['grass', 'fire', 'water', 'bug'],
            "hp": [45, 39, 44, 45],
            "pokedex": ['yes', 'no','yes','no']                        
            }
pokemon = pd.DataFrame(raw_data)
pokemon = pd.DataFrame(raw_data, columns=['name','type','hp','evolution','pokedex'])
pokemon['place'] = ['park','street','lake','forest']
pokemon.dtypes

# exercise 9
path9 = 'Apple_stock.csv'
apple = pd.read_csv(path9)
apple.dtypes
apple.Date = pd.to_datetime(apple['Date'])
apple = apple.set_index('Date')
apple.index.is_unique
apple = apple.sort_index(ascending=True)
apple_month = apple.resample('BM')
temp2 = apple_month.asfreq()[:]
temp = apple_month.interpolate()
(apple.index[-1] - apple.index[0]).days
apple.resample('M').count().shape[0]

# my method
plt.plot(apple.index,apple['Adj Close'])
plt.title('Adj Close plot')
plt.xlabel('Datetime')
plt.ylabel('Adj Close')
plt.show()
# answer
appl_open = apple['Adj Close'].plot(title = "Apple Stock")

# changes the size of the graph
fig = appl_open.get_figure()
fig.set_size_inches(13.5, 9)

# exercise 10
path10 = 'iris.csv'
iris= pd.read_csv(path10,names=['sepal_length','sepal_width', 'petal_length', 'petal_width', 'class'])
iris.isnull().any()
iris.iloc[10:20,2:3] = np.nan
iris = iris.mask(iris.isnull(),1.0)
del iris['class']
iris.iloc[:3,:] = np.nan
iris = iris.dropna(axis=0, how='any')
iris.head()
iris = iris.reset_index(drop=True)
