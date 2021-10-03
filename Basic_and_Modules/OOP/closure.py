# -*- coding: utf-8 -*-
"""
Created on Tue Jun 23 18:15:16 2020

https://www.jb51.net/article/54498.htm

@author: rmileng
"""

# example 1
def createCounter():
    f = [0]
    print('闭包外--')
    def counter():
        print('闭包内--')
        f[0] = f[0] + 1
        return f[0]
    return counter

counterA = createCounter()
print(counterA(), counterA(), counterA(), counterA(), counterA()) # 1 2 3 4 5
counterB = createCounter()
if [counterB(), counterB(), counterB(), counterB()] == [1, 2, 3, 4]:
    print('测试通过!')
else:
    print('测试失败!')


# example 2
def foo():
    name = "python"
    def bar():
        print(name)
        print("hello world in bar")
    return bar
 
f1 = foo()
print(f1.__closure__[0].cell_contents)


# example 3
def foo2():
    print("hello world in foo")
    name = "python"
 
    def bar():
        print(name)
        print("hello world in bar")
    return bar
 
f1 = foo2() # global
 
def func():
    name = "aaaaa"
    f1() # 执行一个闭包函数，这个闭包函数内部引用了name这个变量. 其引用的变量依然是foo函数内部定义的name变量，而不是func函数内部定义的name变量，
    print(name)

func()

## example 4
x_list = [i for i in range(30)]
y_list = [i for i in range(10, 20)]
for y in y_list:
  x_list = list(filter(lambda a: a != y, x_list))
x_list = list(x_list)
print(x_list)
print(len(x_list))

x_list = [i for i in range(30)]
y_list = [i for i in range(10, 20)]
#def check(a,b):
#    print('check')
#    return a!=b

for y in y_list:
    def x_filter(y):
        global x_list
        x_list = filter(lambda x: x != y, x_list)
    x_filter(y)
    print('loop')

x_list = list(x_list)
print(x_list)
print(len(x_list))   


## example 5
# x*=x的左值此时是内部函数作用域里的变量，此时试图将没有定义的数据进行平方操作，因此报错
# 内部函数创建x变量并且屏蔽外部函数作用域内的x变量
def Func1():
   x = 233
   def Func2():
       x *= x
       return x
   return Func2()

# 应用容器类型（list,tuple之类的）存放外部函数作用域的变量从而不会被屏蔽机制屏蔽掉
def Func():
   x = [233]
   def Func2():
       x[0] *= x[0]
       return x[0]
   return Func2()   

def Funcc():
   x = 233
   def Func2():
       nonlocal x
       x *= x
       return x
   return Func2() 

# example 6
def count():
    def f(j):
        def g():
            return j*j
        return g
    fs = []
    for i in range(1,4):        
        fs.append(f(i))
    return fs

f1, f2, f3 = count()
print(f1(), f2(), f3())




















