# -*- coding: utf-8 -*-
"""
Created on Fri Feb  7 11:23:27 2020

@author: rmileng
"""

## lesson 6: group by

# Our small data set
d = {'one':[1,1,1,1,1],
     'two':[2,2,2,2,2],
     'letter':['a','a','b','b','c']}

# Create dataframe
df = pd.DataFrame(d) # key becomes the column value
df
# Create group object
one = df.groupby('letter')

# Apply sum function
one.sum()
letterone = df.groupby(['letter','one']).sum()
letterone
# You may want to not have the columns you are grouping by become your index
letterone = df.groupby(['letter','one'], as_index=False).sum()
letterone
letterone.index