# -*- coding: utf-8 -*-
"""
Created on Fri Jul  3 12:12:22 2020

@author: rmileng
"""

# assert

def foo(s):
    n = int(s)
    assert n != 0, 'n is zero!' # assert的意思是，表达式n != 0应该是True
    return 10 / n

def main():
    foo('0')

