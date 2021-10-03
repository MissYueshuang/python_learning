# -*- coding: utf-8 -*-
"""
Created on Tue Apr  7 17:33:45 2020

@author: rmileng
"""
import pandas as pd
import numpy as np

# 创建一个表示位置（x,y）和颜色（r,g,b）的结构化数组
z = np.zeros(10,[('position',[('x',float,1),('y',float,1)]),
                 ('color',[('r',float,1),('g',float,1),('b',float,1)])])

# equals to enumerate
z = np.arange(9).reshape(3,3)
for index, value in np.ndenumerate(z):
    print(index, value)
for index in np.ndindex(z.shape):
    print(index, z[index])

## generate a Gaussian-like array
X,Y = np.meshgrid(np.linspace(-1,1,10),np.linspace(-1,1,10))
D = np.sqrt(X*X + Y*Y)
sigma, mu = 1, 0
G = np.exp(-((D-mu)**2 / (2*sigma**2)))

## check if an array has a column with 0 value
(~z.any(axis=0)).any()

# class
## create an array with name
class NamedArray(np.ndarray):
    def __new__(cls, array , name="no name"):
        obj = np.asarray(array).view(cls)
        obj.name = name
        return obj
    def __array_finalize__(self,obj):
        if obj is None: return
        self.info = getattr(obj, 'name', 'no name')
Z = NamedArray(np.arange(10),'range_10')
print(Z.name)

# Z[i,j]==Z[j,i]
class Symetric(np.ndarray):
    def __setitem__(self,index,value):
        i,j = index
        super(Symetric,self).__setitem__((i,j),value)
        super(Symetric,self).__setitem__((j,i),value)
def symetric(Z):
    return np.asarray(Z + Z.T - np.diag(Z.diagonal())).view(Symetric)
S = symetric(np.random.randint(0,10,(5,5)))
S[2,3] = 42
print(S[3,2])

## aggregate mean
D = np.random.uniform(0,1,100)
S = np.random.randint(0,10,100)
D_sum = np.bincount(S,weights=D) # aggregate sum
D_counts = np.bincount(S)
D_means = D_sum/D_counts
# or
pd.Series(D).groupby(S).mean()

##
def moving_average(a,n=3):
    ret = np.cumsum(a,dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    return ret[n-1:]/n
z = np.arange(20)

## stride_tricks.as_strided
z = np.random.randint(0,5,(10,10))
n = 3
i = 1 + (z.shape[0] - 3)
j = 1 + (z.shape[1] - 3)
c = np.lib.stride_tricks.as_strided(z,shape=(8,8,n,n),strides=z.strides+z.strides)
print(c)


# 分解出有不全相同值的行
# solution for arrays of all dtypes(including string and record arrays)
z = np.random.randint(0,5,(10,3)) 
e = np.all(z[:,1:] == z[:,:-1],axis=1) # situation 1: all three equals each other
u = z[np.logical_not(e)]
## solution for numerical columns only
u = z[z.max(axis=1)!=z.min(axis=1),:]

## 考虑两个向量A和B，写出用einsum等式对应的inner, outer, sum, mul函数(★★★)
A = np.random.uniform(0,1,10)
B = np.random.uniform(0,1,10)
print('sum')
print(np.einsum('i->',A)) # np.sum(A)

print('A*B')
print(np.einsum('i,i->i',A,B)) # A*B

print('inner')
print(np.einsum('i,i',A,B)) # np.inner(A,B)

print('outer')
print(np.einsum('i,j->ij',A,B)) # np.outer(A,B)

## Given an integer n and a 2D array X, select from X the rows which can be interpreted as 
## draws from a multinomial distribution with n degrees, i.e., the rows which only contain integers and which sum to n
X = np.asarray([[1,0,3,8],[2,0,1,1],[1.5,2.5,1,0]])
n = 4
# method 1
rows = []
for iRow in range(len(X)):
    if (sum(X[iRow])==n) & (sum(np.mod(X[iRow],1))==0):
        rows.append(iRow)
## method 2, better
M = np.logical_and.reduce(np.mod(X,1)==0,axis=-1)
M &= X.sum(axis=-1) == n
print(X[M]) 

# Compute bootstrapped 95% confidence intervals for the mean of a 1D array X，
# i.e. resample the elements of an array with replacement N times, 
# compute the mean of each sample, and then compute percentiles over the means
X = np.random.randn(100) # random 1d array
N = 1000 # number of bootstrap samples
idx = np.random.randint(0,X.size,(N,X.size))
means = X[idx].mean(axis=1)
confint = np.percentile(means,[2.5,97.5])
print(confint)











