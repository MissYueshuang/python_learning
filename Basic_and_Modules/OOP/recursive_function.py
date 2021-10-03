# -*- coding: utf-8 -*-
"""
Created on Thu Jun 18 16:43:08 2020

@author: rmileng
"""

# n!

def fact(n):
    if n==1:
        return 1
    return n * fact(n - 1)

def fact2(n):
    return fact_iter(n, 1)

def fact_iter(num, product):
    if num == 1:
        return product
    return fact_iter(num - 1, num * product)


# 汉诺塔 
def move(n, a, buffer, c):
    if(n == 1):
        print(a,"->",c)
        return
    move(n-1, a, c, buffer)
    move(1, a, buffer, c)
    move(n-1, buffer, a, c)
move(3, "a", "b", "c")

# 编写一个程序，能在当前目录以及当前目录的所有子目录下查找文件名包含指定字符串的文件，
# 并打印出相对路径。
import os

path = r'\\unicorn6\TeamData\VT\CRI_VT_MayBank\\'
string = 'vali_'
#def search_files(path,string):
#    subpath = os.listdir(path)
#    path = [os.path.join(path,l) for l in subpath]
#    for ipath in path:
#        if os.path.isfile(ipath)==False:
#            subpath = os.listdir(ipath)
#            subs = [os.path.join(ipath,isub) for isub in subpath]
#            path.remove(ipath)
#            path.extend(subs)
#    return path
#
#path =  search_file(path,string)
    
def search_file(path,string):
    if string in os.path.split(path)[1]:
        print(os.path.relpath(path))
    if os.path.isfile(path):
        return
    
    for ipath in os.listdir(path):
        search_file(os.path.join(path,ipath),string) # recursive function
        
search_file(path,string) 

# Write a Python program to calculate the sum of the positive integers of n+(n-2)+(n-4)... (until n-x =< 0)
def sumDigits(n):
    if n-2 <= 0 :
        return n
    return n+sumDigits(n-2)
    
sumDigits(10)

# 输入n个数，能自动打印出全排列（Permutation）。比如输入1，2，3，那它的全排列就是123，132，213，231，312，321。
def Permutation(arr):
    if len(arr)<=1:
        return arr
    else:
        temp_list = []
        for i in range(len(arr)):
            for j in Permutation(arr[0:i]+arr[i+1:]):
                temp_list.append(int(str(arr[i])+str(j)))
        return temp_list
    
Permutation([1,2,3,4])  
    
# lst = [1,[2],[[3],4],5], want to return [1, 2, 3, 4, 5]

## standard method
def spread(arg):
    ret = []
    for i in arg:
        if isinstance(i,list):
            ret.extend(i)
        else:
            ret.append(i)
    return ret
    
def deep_flatten(lst):
    result = []
    result.extend(spread(list(map(lambda x:deep_flatten(x) if type (x) == list else x,lst))))
    return result

lst = [1,[2],[[3],4],5]   
deep_flatten(lst)
 
## my method    
def main(lst):
    ret = spread(lst)
    while True in [isinstance(i,list)==True for i in ret]:
        ret = spread(ret)
    return ret 
    
    
    
    
    
    
    
    
    
    
    
    
    
