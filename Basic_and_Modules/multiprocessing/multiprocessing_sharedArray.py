# -*- coding: utf-8 -*-
"""
Created on Mon Feb  3 16:20:18 2020

shared memory 共享内存

@author: rmileng
"""

import multiprocessing as mp

## shared value
value1 = mp.Value('i', 0) 
value2 = mp.Value('d', 3.14) # d表示一个双精浮点类型

## shared array 
array = mp.Array('i', [1, 2, 3, 4]) # 它只能是一维的，不能是多维的, 且需要定义数据形式，否则会报错

| Type code | C Type             | Python Type       | Minimum size in bytes |
| --------- | ------------------ | ----------------- | --------------------- |
| `'b'`     | signed char        | int               | 1                     |
| `'B'`     | unsigned char      | int               | 1                     |
| `'u'`     | Py_UNICODE         | Unicode character | 2                     |
| `'h'`     | signed short       | int               | 2                     |
| `'H'`     | unsigned short     | int               | 2                     |
| `'i'`     | signed int         | int               | 2                     |
| `'I'`     | unsigned int       | int               | 2                     |
| `'l'`     | signed long        | int               | 4                     |
| `'L'`     | unsigned long      | int               | 4                     |
| `'q'`     | signed long long   | int               | 8                     |
| `'Q'`     | unsigned long long | int               | 8                     |
| `'f'`     | float              | float             | 4                     |
| `'d'`     | double             | float             | 8                     |