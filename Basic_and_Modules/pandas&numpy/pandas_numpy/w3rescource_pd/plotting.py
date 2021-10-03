# -*- coding: utf-8 -*-
"""
Created on Wed Nov 18 22:22:10 2020

@author: rmileng
"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv(r'D:\LYS\python_learning\exercise\pandas_numpy\w3rescource\alphabet_stock_data.csv')
df.Date = df.Date.astype('datetime64[ns]')
start_date = pd.to_datetime('2020-4-1')
end_date = pd.to_datetime('2020-09-30') 
df2 = df[(df.Date>=pd.to_datetime('2020-04-01')) & (df.Date<=pd.to_datetime('2020-09-30'))]

# 1. create a line plot of the historical stock prices of Alphabet Inc. between two specific dates.
df.plot('Date','Close',color='green',title='Stock prices of Alphabet Inc.')

# answer                        
new_df = (df['Date']>= start_date) & (df['Date']<= end_date)
df1 = df.loc[new_df]
df2 = df1.set_index('Date')
plt.figure(figsize=(5,5))
plt.suptitle('Stock prices of Alphabet Inc.,\n01-04-2020 to 30-09-2020', \
                 fontsize=18, color='black')
plt.xlabel("Date",fontsize=16, color='black')
plt.ylabel("$ price", fontsize=16, color='black')
 
df2['Close'].plot(color='green');
plt.show()

# 2 a line plot of the opening, closing stock prices of Alphabet Inc. between two specific dates.
df2 = df.loc[(df.Date>=start_date) & (df.Date<=end_date)]
df2.plot('Date',['Close','Open'],title='open and close prices of Alphabet Inc.',color=['red','blue'])

# 3 create a bar plot of the trading volume
plt.figure(figsize=(6,6))
plt.suptitle('Trading Volume of Alphabet Inc. stock,\n01-04-2020 to 30-04-2020', fontsize=16, color='black')
plt.xlabel("Date",fontsize=12, color='black')
plt.ylabel("Trading Volume", fontsize=12, color='black') 
df2.plot('Date','Volume',kind='bar')
plt.show()

# 4. create a bar plot of opening, closing stock prices 
plt.figure(figsize=(15,8))
df2.plot('Date',['Open','Close'],title='close and open prices',rot=20)
plt.ylabel('price in USD')
plt.show()

# 5. create a stacked bar plot of opening, closing stock prices
df2.plot('Date',['Open','Close'],title='close and open prices',kind='bar',stacked=True)

# 6. create a horizontal stacked bar plot of opening, closing stock prices
df2.plot('Date',['Open','Close'],title='close and open prices',kind='barh',stacked=True)

# 7. create a histograms plot of opening, closing, high, low stock prices
plt.figure(figsize=(25,25))
df3 = df2[['Open','Close','High','Low']]
df3.plot.hist(stacked=True,alpha=0.5)
plt.show()

# 9. draw a horizontal and cumulative histograms plot of opening stock prices
df2.Open.plot.hist(orientation='horizontal', cumulative=True)

# 10 create a stacked histograms plot of opening, closing, high, low stock prices
df3.plot.hist(stacked=True,bins=200)
df2[['Open','Close','High','Low']].hist()

# 12 create a plot of stock price and trading volume 
df4 = df2.set_index('Date')

f = plt.figure(figsize=(10,5))
f.subplots_adjust(top=0.85,hspace=2)
f.suptitle('google gragh',fontsize=20)

ax1 = plt.subplot2grid((5,4),(0,0),colspan=5,rowspan=2) 
ax1.plot(df2.Date,df2.Close)
props={'title':'close price plot','ylabel':'price'}
#ax1.set_title('close price plot',pad=10)
#ax1.set_ylabel('price')
ax1.set(**props)

# df4.Close.plot(ax=ax1,kind='line')
ax2 = plt.subplot2grid((5,4),(3,0),colspan=5,rowspan=2) 
ax2.bar(df2.Date,df2.Volume)
ax2.set_title('volume bar plot',pad=10)
ax2.set_ylabel('volume')
# df4.Volume.plot(ax=ax2,kind='bar')
plt.show()

# 13 plot of Open, High, Low, Close, Adjusted Closing prices and Volume
plt.figure(figsize=(10,5))
df4.plot(subplots=True)
plt.suptitle('All')
plt.show()

# 14 create a plot of adjusted closing prices, thirty days and forty days simple moving average
df4['30diff'] = df4['Adj Close'].rolling(window=30).mean()
df4['40diff'] = df4['Adj Close'].rolling(40).mean()
df4[['Adj Close','30diff','40diff']].plot()

# 15 plot of adjusted closing prices, 30 days simple moving average and 20 day exponential moving average
df4['ema'] = df4['Adj Close'].ewm(span=20).mean()
df4[['Adj Close','30diff','ema']].plot()

# 16. create a scatter plot of the trading volume/stock prices
df2.plot(x='Close',y='Volume',kind='scatter')
plt.grid(True)
plt.show()

# 17.  create a plot to visualize daily percentage returns
df2['Return'] = df2['Adj Close'].pct_change()
df2.plot('Date','Return',linestyle='--',marker='v')

# 17 plot the volatility over a period of time of Alphabet Inc. stock price 
df3 = df[['Date', 'Close']].set_index('Date')
data_filled = df3.asfreq('D', method='ffill') # fill weekend data with friday data
data_returns = data_filled.pct_change()
data_std = data_returns.rolling(window=30, min_periods=30).std()
plt.figure(figsize=(20,20))
data_std.plot();
plt.suptitle('Volatility over a period of time  of Alphabet Inc. stock price,\n01-04-2020 to 30-09-2020', fontsize=12, color='black')
plt.grid(True)
plt.show() 

# 19 create a histogram to visualize daily return distribution
sns.distplot(df2.Return.dropna(),hist=True,bins=100,color='purple')















