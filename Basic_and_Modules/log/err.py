# -*- coding: utf-8 -*-
"""
Created on Fri Jul  3 12:21:09 2020

@author: rmileng
"""
# example 1
import logging
logging.basicConfig(level=logging.INFO)
s = '0'
n = int(s)
logging.info('n = %d' % n)
print(10 / n)

# example 2
s = '0'
n = int(s)
print(10 / n)

# examole 3
import pdb
s = '0'
n = int(s)
pdb.set_trace() # 运行到这里会自动暂停
print(10 / n)