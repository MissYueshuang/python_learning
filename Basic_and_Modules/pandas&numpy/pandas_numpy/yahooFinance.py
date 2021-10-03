# -*- coding: utf-8 -*-
"""
Created on Tue Aug 11 17:28:41 2020

@author: rmileng
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from datetime import datetime
from pandas_datareader import data, wb

start = datetime(2015, 1, 1)
end = datetime(2016, 5, 27)
sc = data.DataReader("000001.SS", 'yahoo', start, end) # 000001.SS 表示上证综指，返回 DataFrame
sc.head() # 纵轴是日期，横轴是开盘价、最高价、最低价、收盘价、成交量、复权收盘价。因上证综指并非具体某支股票，所以交易量为 0。
sc.info()

del sc['Volume']
sc.head(2)

fig, ax = plt.subplots(1,1,figsize=(8,4))
sc.plot(ax=ax)
plt.title('SS')
plt.tight_layout()
plt.show()

change = sc.Close.diff()
change.iloc[0] = 0
sc['Change'] = change

sc.Change.plot(kind='line',title='rise and fail')
sc_month = sc.Close.to_period('M').groupby(level=0).mean()
sc_month.plot(kind='bar',title='rise and fail')

url = 'http://data.earthquake.cn/datashare/globeEarthquake_csn.html'
eqs = pd.read_html(io=url,header=0,encoding='gb2312') # encoding 是通过查看网页源代码中的 charset 值得到
eqs[4].head() 

