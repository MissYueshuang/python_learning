# -*- coding: utf-8 -*-
"""
Created on Fri Jan 31 16:32:11 2020

@author: rmileng
"""

import pickle

a_dict = {'da': 111, 2: [23,1,4], '23': {1:2,'d':'sad'}}

# 保存
# pickle a variable to a file
file = open('pickle_example.pickle', 'wb')
pickle.dump(a_dict, file)
file.close() 

# 提取
# reload a file to a variable
with open('pickle_example.pickle', 'rb') as file:
    a_dict1 =pickle.load(file)

print(a_dict1)