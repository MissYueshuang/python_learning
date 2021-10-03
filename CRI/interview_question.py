# -*- coding: utf-8 -*-
"""
Created on Wed Apr  8 16:27:32 2020

@author: rmileng
"""
import numpy as np

def lowertriangle(N):
    mat = np.zeros((N,N))
    mat[:,0] = 1
    for i in range(1,N):
        for j in range(1,i+1):
            mat[i,j] =  sum(mat[:i,j-1])
    return mat