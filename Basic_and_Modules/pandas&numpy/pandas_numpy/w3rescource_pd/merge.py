# -*- coding: utf-8 -*-
"""
Created on Mon Aug 17 14:49:08 2020

@author: rmileng
"""

import pandas as pd

# example1
student_data1 = pd.DataFrame({
        'student_id': ['S1', 'S2', 'S3', 'S4', 'S5'],
         'name': ['Danniella Fenton', 'Ryder Storey', 'Bryce Jensen', 'Ed Bernal', 'Kwame Morin'], 
        'marks': [200, 210, 190, 222, 199]})

student_data2 = pd.DataFrame({
        'student_id': ['S4', 'S5', 'S6', 'S7', 'S8'],
        'name': ['Scarlette Fisher', 'Carla Williamson', 'Dante Morse', 'Kaiser William', 'Madeeha Preston'], 
        'marks': [201, 200, 198, 219, 201]})

df = pd.concat([student_data1,student_data2],axis=0,join='inner')

student_data1.append({'student_id':'S6','name':'Scarlette Fisher','marks':205},ignore_index=True)
student_data1.append(['S6','Scarlette Fisher',205])

# example2
student_data1.index = pd.Index(['a','b','c','d','e'])
student_data2.index = ['A','B','C','D','E']
pd.merge(student_data1,student_data2,on='student_id')

# example2
data1 = pd.DataFrame({'key1': ['K0', 'K0', 'K1', 'K2'],
                     'key2': ['K0', 'K1', 'K0', 'K1'],
                     'P': ['P0', 'P1', 'P2', 'P3'],
                     'Q': ['Q0', 'Q1', 'Q2', 'Q3']}) 
data2 = pd.DataFrame({'key1': ['K0', 'K1', 'K1', 'K2'],
                      'key2': ['K0', 'K0', 'K0', 'K0'],
                      'R': ['R0', 'R1', 'R2', 'R3'],
                      'S': ['S0', 'S1', 'S2', 'S3']})
pd.concat([data1,data2],ignore_index=True)

# example4
# by filling null values in one DataFrame with non-null values from other DataFrame.
df1 = pd.DataFrame({'A': [None, 0, None], 'B': [3, 4, 5]})
df2 = pd.DataFrame({'A': [1, 1, 3], 'B': [3, None, 3]})
df1.combine_first(df2)

df1 = pd.DataFrame({'A': [0, 0], 'B': [None, 4]})
df2 = pd.DataFrame({'A': [1, 1], 'B': [None, 3]})
take_smaller = lambda s1, s2: s1 if s1.sum() < s2.sum() else s2
df1.combine_first(df2, take_smaller, fill_value=-5)

df1 = pd.DataFrame({'A': [None, 0], 'B': [4, None]})
df2 = pd.DataFrame({'B': [3, 3], 'C': [1, 1]}, index=[1, 2])
df1.combine_first(df2)



