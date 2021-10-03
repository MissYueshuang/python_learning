# -*- coding: utf-8 -*-
"""
Created on Mon Feb  3 16:03:47 2020

@author: rmileng
"""

## pool: 进程池
import multiprocessing as mp

def job(x): # 可以用return now
    return x*x

def multicore():
    pool = mp.Pool(processes=2) # use n cores, 自动分配给CPU核，返回结果
    res = pool.map(job, range(10))
    print(res)
    res = pool.apply_async(job, (2,))
    print(res.get())
    multi_res =[pool.apply_async(job, (i,)) for i in range(10)]
    print([res.get() for res in multi_res])

if __name__ == '__main__':
    multicore()
    
## apply_async()中只能传递一个值，它只会放入一个核进行运算，但是传入值时要注意是可迭代的，所以在传入值后需要加逗号, 同时需要用get()方法获取返回值