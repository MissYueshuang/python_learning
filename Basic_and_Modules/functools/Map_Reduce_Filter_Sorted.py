# -*- coding: utf-8 -*-
"""
Created on Thu Jun 18 19:56:32 2020

@author: rmileng
"""
#import myPythonTools
# from myPythonTools.value_Comparison import value_Comparison ##This is how to call my package
from functools import reduce
import numpy as np

# map
r = map(lambda x: x*2, [1, 2, 3, 4, 5, 6, 7, 8, 9])

# reduce
## define your own function the same as 'int'
# method 1
def func1(x,y):
    return x*10+y
def func2(s):
    digits = {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9}
    return digits[s]
reduce(func1,map(func2,'13579'))

# method 2: only one function
def str2int(s):
    def fn(x, y):
        return x * 10 + y
    def char2num(s):
        return digits[s]
    return reduce(fn, map(char2num, s))

# method 3: using lambda
digits = {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9}
def str2int2(s):
    num = map(lambda s: digits[s], s)
    return reduce(lambda x,y: x*10+y, num)

def normalize(L):
    return list(map(lambda s: s[0].upper() + s[1:].lower(),L))

def str2float(s):
    idx = s.index('.')
    num = list(map(lambda s: digits[s] if s !='.' else 0, s))
    part1 = reduce(lambda x,y: x*10+y,num[:idx])
    part2 = reduce(lambda x,y: x*0.1+y,num[idx:][::-1])
    return part1+part2

# 用filter求素数

## my method
L = list(range(3,40))
def is_odd(li):
    return lambda n: n % li[0] != 0 
i=0
result = []
while i<=len(L):
    result.append(L[0])
    L = list(filter(is_odd(L),L)) # filter only accept one parameter
    i += 1
print(result)

# official methods
def _odd_iter():
    n=1
    while n<100 : # or while True if you want an infinite sequence
        n = n+2
        yield n

def _not_divisible(n):
    return lambda x: x % n > 0

def primes():
    yield 2
    it = _odd_iter()
    while True: # while True means always true, means do it forever
        n = next(it)
        it = filter(_not_divisible(n),it)

for n in primes():
    if n<100:
        print(n)
    else:
        break

# 回数是指从左向右读和从右向左读都是一样的数，例如12321，909。请利用filter()筛选出回数：
L = range(1, 1000)
def is_palindrome(n):
    string = str(n)
    if string == string[::-1]:
        return n      

re = filter(is_palindrome,L)


L = [('Bob', 75), ('Adam', 92), ('Bart', 66), ('Lisa', 88)]
def by_name(t):
    return t[0]
L2 = sorted(L, key=by_name)
print(L2)






      