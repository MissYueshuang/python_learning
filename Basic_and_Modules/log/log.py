# -*- coding: utf-8 -*-
"""
Created on Mon Jun 29 16:59:38 2020

@author: rmileng
"""
## 注意，这里文件名不能保存为Logging，否则import logging会import自身这个文件（一个文件就是一个Module）
import logging
logging.basicConfig(filename=r'D:\LYS\temp files\my.log', level=logging.ERROR)

def foo(s):
    return 10 / int(s)

def bar(s):
    return foo(s) * 2

def main():
    try:
        bar('0')
    except Exception as e:
        logging.error(e)

if __name__=='__main__':
    main()


# example 2
'''
为什么前面两条日志没有被打印出来？
这是因为logging模块提供的日志记录函数所使用的日志器设置的日志级别是WARNING，
因此只有WARNING级别的日志记录以及大于它的ERROR和CRITICAL级别的日志记录被输出了，
而小于它的DEBUG和INFO级别的日志记录被丢弃了。
'''
logging.log(logging.DEBUG, "This is a debug log.")
logging.log(logging.INFO, "This is a info log.")
logging.log(logging.WARNING, "This is a warning log.")
logging.log(logging.ERROR, "This is a error log.")
logging.log(logging.CRITICAL, "This is a critical log.")
