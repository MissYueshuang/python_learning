# -*- coding: utf-8 -*-
"""
Created on Fri Feb  7 11:22:39 2020

@author: rmileng
"""

## lesson 5: Stack/Unstack/Transpose functions
d = {'one':[1,1],'two':[2,2]}
i = ['a','b']
df = pd.DataFrame(data = d, index = i)
df
# Bring the columns and place them in the index
stack = df.stack()
stack
# The index now includes the column names
stack.index
unstack = df.unstack()
unstack
# transpose
transpose = df.T
transpose