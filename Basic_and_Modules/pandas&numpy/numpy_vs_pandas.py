# -*- coding: utf-8 -*-
"""
Created on Tue Feb 25 11:33:11 2020

numpy vs pandas

@author: rmileng
"""

'''
numpy consumes less memory compared to pandas
numpy generally performs better than pandas for 50K rows or less
pandas generally performs better than numpy for 500K rows or more
for 50K to 500K rows, it is a toss up between pandas and numpy depending on the kind of operation
'''
import pandas as pd
import matplotlib.pyplot as plt
import seaborn.apionly as sns
import numpy as np
from timeit import timeit 
import sys

iris = pd.read_csv(r'D:\LYS\python_learning\result_files\iris.csv')
data = pd.concat([iris]*100000)
data_rec = data.to_records() # The to_records() function is used to convert DataFrame to a NumPy record array.
print (len(data), len(data_rec))

MB = 1024*1024
print("Pandas %d MB " % (sys.getsizeof(data)/MB)) # 1506 MB 
print("Numpy %d MB " % (sys.getsizeof(data_rec)/MB)) # 686 MB 

bench(data, "data.loc[:, 'sepal_length'].mean()", 
      data_rec, "np.mean(data_rec.sepal_length)",
     title="Mean on Unfiltered Column")