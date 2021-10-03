# -*- coding: utf-8 -*-
"""
Created on Mon Aug 10 16:38:22 2020

@author: rmileng
"""

from collections import Counter

c1 = Counter('asdf')
c2 = Counter('adfs')
c1 == c2
a = [1,2,34]
list(filter(lambda x: x<10, a))
array = [['a','b'],['c','d'],['e','f']]
list(zip(*array))

def vowel(string):
    c = Counter(string)    
    popkeys = [i for i in c if i not in 'aeiou']
    [c.pop(i) for i in popkeys]
    return dict(c)

list1 = [3,4,5]
list2 = [1,3,4,2,3]

def difference(list1,list2):
    return set(list1).difference(set(list2))

def difference_by(a,b,fn):
    b = set(map(fn,b))
    return [i for i in a if fn(i) not in b]

from math import floor
difference_by([2.1,1.2],[2.3,3.4],floor)

# 链式调用函数
def add(a,b):
    return a+b
def substract(a,b):
    return a-b
a,b = 4,5
print((substract if a > b else add)(a,b))

# list to dict
keys = ['a','b','c']
values = [1,2,3]
dict((zip(keys,values)))

# enumerate
for index, value in enumerate(keys):
    print(index,value)
    
# freq
def most_frequent(lst):
    return max(set(lst),key=lst.count)    
lst = [1,2,3,3,4,2,5,3,5]
most_frequent(lst)

# 回文序列
string = 'adfSRsdf1243_!'
def huiwen(string):
    string = string.lower()
    s = ''.join([i for i in string if ord(i) in range(ord('a'),ord('z'))])
    return s == s[::-1]
    











    
