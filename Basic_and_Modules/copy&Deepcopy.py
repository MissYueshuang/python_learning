# -*- coding: utf-8 -*-
"""
Created on Fri Jan 31 15:40:08 2020

@author: rmileng
"""
# id
import copy
a=[1,2,3]
b=a # identical, a change with b 
id(a) 
"""
4382960392
"""
id(b)
"""
4382960392
"""
id(a)==id(b)    #附值后，两者的id相同，为true。
True

b[0]=222222  #此时，改变b的第一个值，也会导致a值改变。
print(a,b)
[222222, 2, 3] [222222, 2, 3] #a,b值同时改变


# 浅层拷贝
a=[1,2,3]
c=copy.copy(a)  #拷贝了a的外围对象本身,
id(c)
4383658568
print(id(a)==id(c))  #id 改变 为false
False

c[1]=22222   #此时，我去改变c的第二个值时，a不会被改变。
print(a,c)
[1, 2, 3] [1, 22222, 3] #a值不变,c的第二个值变了，这就是copy和‘==’的不同

## 深拷贝
#copy.copy()

a=[1,2,[3,4]]  #第三个值为列表[3,4],即内部元素
d=copy.copy(a) #浅拷贝a中的[3，4]内部元素的引用，非内部元素对象的本身
id(a)==id(d)
False
id(a[2])==id(d[2])
True
a[2][0]=3333  #改变a中内部原属列表中的第一个值
d             #这时d中的列表元素也会被改变
[1, 2, [3333, 4]]


 

e=copy.deepcopy(a) #e为深拷贝了a
a[2][0]=333 #改变a中内部元素列表第一个的值
e
[1, 2, [3333, 4]] #因为时深拷贝，这时e中内部元素[]列表的值不会因为a中的值改变而改变