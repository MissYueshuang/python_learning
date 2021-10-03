# -*- coding: utf-8 -*-
"""
Created on Fri Jul  3 11:51:27 2020

@author: rmileng
"""
from functools import reduce
# example 1
def str2num(s):
    try:
        return int(s)
    except ValueError as e:
        print('ValueError',e)
    finally:
        return float(s)

def calc(exp):
    ss = exp.split('+')
    ns = map(str2num, ss)
    return reduce(lambda acc, x: acc + x, ns)

def main():
    r = calc('100 + 200 + 345')
    print('100 + 200 + 345 =', r)
    r = calc('99 + 88 + 7.6')
    print('99 + 88 + 7.6 =', r)

main()

# example 2
try:
    10 / 0
except ZeroDivisionError:
    raise ValueError('input error!')
    
# example 3
def foo(s):
    n = int(s)
    if n==0:
        raise ValueError('invalid value: %s' % s)
    return 10 / n

def bar():
    try:
        foo('0')
    except ValueError as e:
        print('ValueError!')
        raise

bar()



