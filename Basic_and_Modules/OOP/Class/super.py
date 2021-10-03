# -*- coding: utf-8 -*-
"""
Created on Wed Jul 22 15:43:48 2020

@author: rmileng
"""

# 多重继承的执行顺序,请解答以下输出结果是什么？
class A(object):
   def __init__(self):
       print('A')
       super(A, self).__init__()

class B(object):
   def __init__(self):
       print('B')
       super(B, self).__init__()

class C(A):
   def __init__(self):
       print('C')
       super(C, self).__init__()

class D(A):
   def __init__(self):
       print('D')
       super(D, self).__init__()

class E(B, C):
   def __init__(self):
       print('E')
       super(E, self).__init__()

class F(C, B, D):
   def __init__(self):
       print('F')
       super(F, self).__init__()

class G(D, B):
   def __init__(self):
       print('G')
       super(G, self).__init__()                                                                                                                                                                                                                                                                                       
g = G()
G.mro()

if __name__ == '__main__':
   g = G()
   f = F()
   
# super 2
# https://wiki.jikexueyuan.com/project/explore-python/Class/super.html
class Base(object):
    def __init__(self):
        print("enter Base")
        print("leave Base")

class A(Base):
    def __init__(self):
        print("enter A")
        super(A, self).__init__()
        print("leave A")

class B(Base):
    def __init__(self):
        print("enter B")
        super(B, self).__init__()
        print("leave B")

class C(A, B):
    def __init__(self):
        print("enter C")
        super(C, self).__init__()
        print("leave C")

c = C()
C.mro()

# example 3： 调用父类构造函数
# https://blog.csdn.net/lovemysea/article/details/78836927
class A:
    def __init__(self):
        self.namea="aaa"
 
    def funca(self):
        print("function a : %s"%self.namea)
 
class B(A):
    def __init__(self):
#        A.__init__(self) # 方法一
        super(B,self).__init__() # 方法二
        self.nameb="bbb"
 
    def funcb(self):
        print("function b : %s"%self.nameb)
 
b=B()
print(b.nameb)
b.funcb()
'''
子类其实是重写了父类的构造函数，如果不显式调用父类构造函数，
父类的构造函数就不会被执行，导致子类实例访问父类初始化方法中初始的变量就会出现问题。
''' 
b.funca()
