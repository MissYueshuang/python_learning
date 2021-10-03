# -*- coding: utf-8 -*-
"""
Created on Mon Feb  3 14:29:45 2020

@author: rmileng
"""
### you have to run this in cmd

import multiprocessing as mp

def job(q):
    res = 0
    for i in range(1000):
        res += i+i**2+i**3
    q.put(res)
    
    
if __name__=='__main__':
    q = mp.Queue() # queue中的东西先放先得（左移动）
    p1 = mp.Process(target=job,args=(q,)) # 定义两个线程函数，用来处理同一个任
    p2 = mp.Process(target=job,args=(q,)) # args 的参数只要一个值的时候，参数后面需要加一个逗号，表示args是可迭代的，后面可能还有别的参数，不加逗号会出错
    p1.start()
    p2.start()
    p1.join()
    p2.join()
    res1 = q.get() # 分两批输出，将结果分别保存
    res2 = q.get()
    print(res1+res2)


