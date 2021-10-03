# -*- coding: utf-8 -*-
"""
Created on Mon Feb 24 16:45:27 2020

@author: rmileng
"""
import pandas as pd
import numpy as np

s = pd.Series([1,3,6,np.nan,44,1])
dates = pd.date_range('20160101',periods=6)
df = pd.DataFrame(np.random.randn(6,4),index=dates,columns = ['a','b','c','d'])
df1 = pd.DataFrame(np.arange(12).reshape((3,4))) # 如果不指定Index 和columns
df2 = pd.DataFrame({'A' : 1., ## 自动补齐4行
                    'B' : pd.Timestamp('20130102'),
                    'C' : pd.Series(1,index=list(range(4)),dtype='float32'),
                    'D' : np.array([3] * 4,dtype='int32'),
                    'E' : pd.Categorical(["test","train","test","train"]), # Represent a categorical variable in classic R / S-plus fashion.
                    'F' : 'foo'})                  
print(df2)
df2.dtypes
df2.index
df2.columns # 不需要括号，因为是一个属性，不是方法
df2.values
df2.describe()
df2.T
df2.sort_index(axis=0,ascending=False)
df2.sort_values(by='E')

## 选择数据(index)
dates = pd.date_range('20130101',periods=6)
df = pd.DataFrame(np.arange(24).reshape((6,4)),index=dates, columns=['A','B','C','D'])
print(df['A'],df.A) # the same, select column
print(df[0:3],df['20130101':'20130103']) # the same, select index

# mix position and label
print(df.ix[:3,['A','C']])
print(df[df.A<8])

# 设置值
df.B[df.A>4] = 0 # 如果A列大于4,则将B列的数据改成0

## 处理queshizhi
df.iloc[0,1] = np.nan
df.iloc[1,2] = np.nan

df.dropna(axis=1,how='any') # how = any or all. and it will not change the orginal df unless you use df=df.dropna(axis=1,how='any')
df.fillna(value=0)
np.any(df.isnull())

## pandas 导入导出
'''
format: read_x/to_x
'''
df.to_pickle('df.pickle')

## 合并 concat
df1 = pd.DataFrame(np.ones((3,4))*0, columns=['a','b','c','d'])
df2 = pd.DataFrame(np.ones((3,4))*1, columns=['a','b','c','d'])
df3 = pd.DataFrame(np.ones((3,4))*2, columns=['a','b','c','d'])

res = pd.concat([df1, df2, df3], axis=0, ignore_index=True)
print(res)

#定义资料集, columns are index are different
df1 = pd.DataFrame(np.ones((3,4))*0, columns=['a','b','c','d'], index=[1,2,3])
df2 = pd.DataFrame(np.ones((3,4))*1, columns=['b','c','d','e'], index=[2,3,4])
#纵向"外"合并df1与df2
res = pd.concat([df1, df2], axis=0, join='inner',ignore_index=True)
print(res)

# join_axes
res = pd.concat([df1, df2], axis=1, join_axes=[df1.index])

# append
df1 = pd.DataFrame(np.ones((3,4))*0, columns=['a','b','c','d'])
df2 = pd.DataFrame(np.ones((3,4))*1, columns=['a','b','c','d'])
df3 = pd.DataFrame(np.ones((3,4))*1, columns=['b','c','d', 'e'], index=[2,3,4])
res = df1.append(df2, ignore_index=True)
res = df1.append([df2, df3])

s1 = pd.Series([1,2,3,4], index=['a','b','c','d'])
res = df1.append(s1, ignore_index=True)

print(res)

############################################################################### merge
#from __future__ import print_function
import pandas as pd

# merging two df by key/keys. (may be used in database)
# simple example
left = pd.DataFrame({'key': ['K0', 'K1', 'K2', 'K3'],
                     'A': ['A0', 'A1', 'A2', 'A3'],
                     'B': ['B0', 'B1', 'B2', 'B3']})
right = pd.DataFrame({'key': ['K0', 'K1', 'K2', 'K3'],
                      'C': ['C0', 'C1', 'C2', 'C3'],
                      'D': ['D0', 'D1', 'D2', 'D3']})
print(left)
print(right)
res = pd.merge(left, right, on='key')
print(res)

# consider two keys
left = pd.DataFrame({'key1': ['K0', 'K0', 'K1', 'K2'],
                     'key2': ['K0', 'K1', 'K0', 'K1'],
                     'A': ['A0', 'A1', 'A2', 'A3'],
                     'B': ['B0', 'B1', 'B2', 'B3']})
right = pd.DataFrame({'key1': ['K0', 'K1', 'K1', 'K2'],
                     'key2': ['K0', 'K0', 'K0', 'K0'],
                     'C': ['C0', 'C1', 'C2', 'C3'],
                     'D': ['D0', 'D1', 'D2', 'D3']})
print(left)
print(right)
res = pd.merge(left, right, on=['key1', 'key2'], how='inner')  # default for how='inner'
# how = ['left', 'right', 'outer', 'inner']
res = pd.merge(left, right, on=['key1', 'key2'], how='left')
print(res)

# indicator
df1 = pd.DataFrame({'col1':[0,1], 'col_left':['a','b']})
df2 = pd.DataFrame({'col1':[1,2,2],'col_right':[2,2,2]})
print(df1)
print(df2)
res = pd.merge(df1, df2, on='col1', how='outer', indicator=True)
# give the indicator a custom name
res = pd.merge(df1, df2, on='col1', how='outer', indicator='indicator_column')


# merged by index
left = pd.DataFrame({'A': ['A0', 'A1', 'A2'],
                     'B': ['B0', 'B1', 'B2']},
                     index=['K0', 'K1', 'K2'])
right = pd.DataFrame({'C': ['C0', 'C2', 'C3'],
                      'D': ['D0', 'D2', 'D3']},
                      index=['K0', 'K2', 'K3'])
print(left)
print(right)
# left_index and right_index
res = pd.merge(left, right, left_index=True, right_index=True, how='outer')
res = pd.merge(left, right, left_index=True, right_index=True, how='inner')

# handle overlapping
boys = pd.DataFrame({'k': ['K0', 'K1', 'K2'], 'age': [1, 2, 3]})
girls = pd.DataFrame({'k': ['K0', 'K0', 'K3'], 'age': [4, 5, 6]})
print(boys)
print(girls)
res = pd.merge(boys, girls, on='k', how='inner') # default on age_x, age_y
print(res)
res = pd.merge(boys, girls, on='k', suffixes=['_boy', '_girl'], how='inner')
print(res)

# join function in pandas is similar with merge. If know merge, you will understand join
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# plot data

# Series
data = pd.Series(np.random.randn(1000), index=np.arange(1000))
data = data.cumsum()
data.plot()
plt.show()

# DataFrame
data = pd.DataFrame(np.random.randn(1000, 4), index=np.arange(1000), columns=list("ABCD"))
data = data.cumsum()
data.plot()
plt.show()

# plot methods:
# 'bar', 'hist', 'box', 'kde', 'area', 'scatter', 'hexbin', 'pie'
ax = data.plot.scatter(x='A', y='B', color='DarkBlue', label="Class 1")
data.plot.scatter(x='A', y='C', color='LightGreen', label='Class 2', ax=ax)
plt.show()
















