# -*- coding: utf-8 -*-
"""
Created on Thu Jan 16 17:13:46 2020

@author: rmileng
"""

a = [9,9,9,9]

def test(a):
    temp1 = int(''.join([str(i) for i in a])) + 2
    out = [int(str(temp1)[i]) for i in range(len(str(temp1)))]
    print(out)