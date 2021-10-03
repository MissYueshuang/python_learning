# -*- coding: utf-8 -*-
"""
Created on Wed Jan  8 11:44:05 2020

@author: rmileng
"""

# Lesson 4: Adding/deleting columns - Index operations
import pandas as pd
import sys

d = [0,1,2,3,4,5,6,7,8,9]

# Create dataframe
df = pd.DataFrame(d)
df.columns = ['Rev']

# Lets add a column
df['NewCol'] = 5
df
df['NewCol'] = df['NewCol'] + 1
df
del df['NewCol']
df
df['test'] = 3
# Lets add a couple of columns
df['col'] = df['Rev']
df
# If we wanted, we could change the name of the index
i = ['a','b','c','d','e','f','g','h','i','j']
df.index = i
df


# index!!
df.loc['a']
df.loc['a':'d']
df.iloc[0:3]
df['Rev']
df[['Rev', 'test']]
df.loc[df.index[0:3],'Rev']
















