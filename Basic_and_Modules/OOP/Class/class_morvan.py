# -*- coding: utf-8 -*-
"""
Created on Thu Jan 30 17:38:42 2020

@author: rmileng
"""
# class 定义一个类, 后面的类别首字母推荐以大写的形式定义，比如Calculator. class可以先定义自己的属性，
# 比如该属性的名称可以写为 name='Good Calculator'. class后面还可以跟def, 定义一个函数. 
# 比如def add(self,x,y): 加法, 输出print(x+y). 其他的函数定义方法一样，注意这里的self 是默认值.

class Calculator:       #首字母要大写，冒号不能缺
    name='Good Calculator'  #该行为class的属性
    price=18
    def add(self,x,y):
        print(self.name)
        result = x + y
        print(result)
    def minus(self,x,y):
        result=x-y
        print(result)
    def times(self,x,y):
        print(x*y)
    def divide(self,x,y):
        print(x/y)

""""
>>> cal=Calculator()  #注意这里运行class的时候要加"()",否则调用下面函数的时候会出现错误,导致无法调用.
>>> cal.name
'Good Calculator'
>>> cal.price
18
>>> cal.add(10,20)
Good Calculator
30
>>> cal.minus(10,20)
-10
>>> cal.times(10,20)
200
>>> cal.divide(10,20)
0.5
""""


# __init__可以理解成初始化class的变量，取自英文中initial 最初的意思.可以在运行时，给初始值附值，
# 运行c=Calculator('bad calculator',18,17,16,15),然后调出每个初始值的值。看如下代码。

class Calculator:
    name='good calculator'
    price=18
    def __init__(self,name,price,height,width,weight=90):   # 注意，这里的下划线是双下划线
        self.name=name
        self.price=price
        self.h=height # you can change the name
        self.wi=width
        self.we=weight
    def add(self,x,y):
        print(self.name)
        result = x + y
        print(result)
    def minus(self,x,y):
        result=x-y
        print(result)
    def times(self,x,y):
        print(x*y)
    def divide(self,x,y):
        print(x/y)
""""
>>> c=Calculator('bad calculator',18,17,16,15) # you must input 5 paras
>>> c.name # 
'bad calculator'
>>> c.price
18
>>> c.h
17
>>> c.wi
16
>>> c.we
15
>>>c.add(10,11)
""""