# -*- coding: utf-8 -*-
"""
Created on Wed Feb 12 17:28:34 2020

@author: rmileng
"""
import numpy as np

def ismember(A,B): # A and B are arrays
    result = np.in1d(A,B)
    idxT = []
    idxF = []     
    for i in range(len(result)):
        if result[i]==True:
            idxT.append(i)
        else:
            idxF.append(i)
    return result,idxT,idxF ## index are row numbers , not acutally the index number 