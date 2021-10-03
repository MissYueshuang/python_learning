# -*- coding: utf-8 -*-
"""
Created on Sun Apr 18 16:38:47 2021

@author: ys.leng
"""

# method 1
L = [2,2,5,7,45,2,6,2,22,2,2,2,2,2,2,2]
x = 2

L1 = []
L2 = []
for si in L:
    if si == x:
        L1.append(si)
    else:
        L2.append(si)
        
L2+L1

# mthod 2
i,q = 0,0
while q <= len(L):
    si = L[i]
    if si == x:
        L.pop(i)
        L.append(si)
        i += -1
    i += 1
    q += 1
L
q

# method 3
L = [2,2,5,7,45,2,6,2,22,2,2,2,2,2,2,2,1]
i = 0
while i <= len(L):
    si = L[i]
    if si == x:
        L.pop(i)
        L.append(si)
        i += -1
    i += 1
    if len(set(L[i:-1])) == 1:
        break
L
i

