# -*- coding: utf-8 -*-
"""
Created on Tue Jul 14 16:47:42 2020

@author: rmileng
"""

matrix = [
     [1, 2, 3, 4],
     [5, 6, 7, 8],
     [9, 10, 11, 12],
 ]

# transpose
[[row[i] for row in matrix] for i in range(4)]