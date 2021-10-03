# -*- coding: utf-8 -*-
"""
Created on Mon Jun 15 11:39:23 2020

@author: rmileng
"""

'''
利用切片操作，实现一个trim()函数，去除字符串首尾的空格，注意不要调用str的strip()方法
'''
def trim(s):
    if len(s) != 0:        
        idx = [i.isspace() for i in s]
        if all(idx) == False:
            start_idx = idx.index(0) 
            end_index = idx[::-1].index(0) * (-1)
            if end_index == 0:
                end_index = len(s)+1
            s = s[start_idx:end_index]
        else:
            s = ''
    return s

def trim2(s):
    while s[:1] == ' ':
        s = s[1:]
    while s[-1:] == ' ':
        s = s[0:-1]
    return s
'''
此方法会有一个问题，当字符串仅仅是一个空格时‘ ’，会返回return s[1:0]；虽然不会报错，但是会比较奇怪
'''
def trim3(s):
    i = 0
    j = len(s) - 1
    while i < len(s):
        if s[i] == ' ':
            i = i + 1
        else:
            break
    while j > -1:
        if s[j] == ' ':
            j = j - 1
        else:
            break
    return s[i:j+1]

if trim('hello  ') != 'hello':
    print('测试失败!')
elif trim('  hello') != 'hello':
    print('测试失败!')
elif trim('  hello  ') != 'hello':
    print('测试失败!')
elif trim('  hello  world  ') != 'hello  world':
    print('测试失败!')
elif trim('') != '':
    print('测试失败!')
elif trim('    ') != '':
    print('测试失败!')
else:
    print('测试成功!')