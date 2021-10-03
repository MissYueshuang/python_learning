# -*- coding: utf-8 -*-
"""
Created on Wed Jan 13 11:39:43 2021

@author: rmileng
"""
import os
import logging
import time

def log(func):
    def wrapper(*args, **kwatgs):
        VTname = os.environ['COMPUTERNAME']
        logger = logging.getLogger()
        logger.setLevel(level=logging.INFO)
        handler = logging.FileHandler('log.txt', mode='a')
        handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
        handler.setLevel(logging.INFO)
        for h in logger.handlers:
            logger.removeHandler(h) # 移除其他所有的handler
        logger.addHandler(handler) # 设置新的handler
        
        start_time = time.time()
     #   logger.info('start %s()' % func.__name__)
        econ = func(*args, **kwatgs)
        end_time = time.time()                
        logger.info('cost {:.5f} minutes for econ {} on {}'.format((end_time - start_time)/60,econ,VTname))
#        return ret
    return wrapper


@log
def add(a, b):
    return a

os.chdir(r'D:\LYS\temp files')
add(1,2)

