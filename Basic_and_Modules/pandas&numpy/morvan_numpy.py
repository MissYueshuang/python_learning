# -*- coding: utf-8 -*-
"""
Created on Mon Feb 24 14:29:14 2020
Morvan

@author: rmileng
"""
import numpy as np

## attributes
# 把矩阵定义为array
array = np.array([[1,2,3],
                  [2,3,4]])

print('number of dim:',array.ndim)  # 维度
# number of dim: 2

print('shape :',array.shape)    # 行数和列数
# shape : (2, 3)

print('size:',array.size)   # 元素个数
# size: 6

## 创建array
a = np.array([2,23,4],dtype=np.int) # numpy的type是dtype
print(a.dtype)
## 创建特定数据
a = np.zeros((3,4)) # 数据全为0，3行4列
a = np.empty((3,4)) # 数据为empty，3行4列
a = np.arange(10,20,2) # 10-19 的数据，2步长
a = np.arange(12).reshape((3,4))    # 3行4列，0到11
a = np.linspace(1,10,20)    # 开始端1，结束端10，且分割成20个数据，生成线段

## numpy的基础运算
a = np.array([10,20,30,40])
b = np.arange(4)
c = a-b ## a,b的元素逐个相加减乘除
c = b**2
c = 10*np.sin(a)
print(b<3) # [ True  True  True False]

a = np.array([[1,1],[0,1]])
b = np.arange(4).reshape((2,2))
c = a*b
c_dot = np.dot(a,b)
c_dot2 = a.dot(b)
print(c)
print(c_dot)

a = np.random.random((2,4)) # 随机返回0-1的数据，括号里是shape
np.sum(a,axis=1) # by row
np.max(a,axis=0) #by column

A = np.arange(2,14).reshape((3,4)) 
np.argmin(A) ## 最小值的索引
np.argmax(A) ## 最小值的索引
A.mean()
np.mean(A)
np.cumsum(A)
np.diff(A)
np.clip(A,5,9) # 截取

## numpy 索引
A = np.arange(3,15).reshape((3,4))
A[1][1] # 8
A[1,1]
for row in A: # 默认迭代每一行
    print(row)
## 不能直接迭代每一列，实现的方法：
for column in A.T:
    print(column) # 迭代每一列
A.flatten()
for item in A.flat:
    print(item) # 迭代每一个

## array 合并
A = np.array([1,1,1]) # A只是一个序列，没有第二个shape
A.shape # (3,)
B = np.array([2,2,2])
C = np.vstack((A,B)) # vertical stack
D = np.hstack((A,B)) # vertical stack
print(A.T.shape) # 不能用transpose把一个横向的序列变成一个纵向的序列

print(A[np.newaxis,:])
# [[1 1 1]]

print(A[np.newaxis,:].shape)
# (1,3)

print(A[:,np.newaxis])
"""
[[1]
[1]
[1]]
"""

print(A[:,np.newaxis].shape)
# (3,1)

A = np.array([1,1,1])[:,np.newaxis]
B = np.array([2,2,2])[:,np.newaxis]
         
C = np.vstack((A,B))   # vertical stack
D = np.hstack((A,B))   # horizontal stack

print(D)
"""
[[1 2]
[1 2]
[1 2]]
"""
print(A.shape,D.shape)
# (3,1) (3,2)

C = np.concatenate((A,B,B,A),axis=1)

### array分割
A = np.arange(12).reshape((3, 4))
np.split(A,4,axis=1) ## can only split equally
np.array_split(A,3,axis=1) ## can only split not equally
np.hsplit(A,2)
np.vsplit(A,3)

############################################# speed up
import time
'''
(“C-type”/”Fortran”)
'''
a = np.zeros((200, 200), order='C') #  a 是用 row 为主的形式储存, 所以在 row 上面选数据要比在 column 上选快很多!
b = np.zeros((200, 200), order='F')
N = 9999

def f1(a):
    for _ in range(N):
        np.concatenate((a, a), axis=0)

def f2(b):
    for _ in range(N):
        np.concatenate((b, b), axis=0)

t0 = time.time()
f1(a)
t1 = time.time()
f2(b)
t2 = time.time()

print((t1-t0)/N)     # 0.000040
print((t2-t1)/N)     # 0.000070

np.vstack((a,a))                # 0.000063
np.concatenate((a,a), axis=0)   # 0.000040

####### copy慢，view快
a = np.arange(1, 7).reshape((3,2))
a_view = a[:2]
a_copy = a[:2].copy()

a_copy[1,1] = 0
print(a)
"""
[[1 2]
 [3 4]
 [5 6]]
"""

a_view[1,1] = 0
print(a)
"""
[[1 2]
 [3 0]
 [5 6]]
"""
# 因为 view 不会复制东西, 速度快!
a = np.zeros((1000, 1000))
b = np.zeros((1000, 1000))
N = 9999

def f1(a):
    for _ in range(N):
        a *= 2           # same as a[:] *= 2

def f2(b):
    for _ in range(N):
        b = 2*b

print('%f' % ((t1-t0)/N))     # f1: 0.000837
print('%f' % ((t2-t1)/N))     # f2: 0.001346
## 上面的例子中 a*=2 就是将这个 view 给赋值了, 和 a[:] *= 2 一个意思, 从头到尾没有创建新的东西. 而 b = 2*b 中, 我们将 b 赋值给另外一个新建的 b.

def f1(a):
    for _ in range(N):
        a.flatten()

def f2(b):
    for _ in range(N):
        b.ravel()

print('%f' % ((t1-t0)/N))    # 0.001059
print('%f' % ((t2-t1)/N))    # 0.000000
## ravel 返回的是一个 view ，flatten 返回的总是一个 copy. 相比于 flatten, ravel 是神速.

## 选择数据
# view
a_view1 = a[1:2, 3:6]    # 切片 slice
a_view2 = a[:100]        # 同上
a_view3 = a[::2]         # 跳步
a_view4 = a.ravel()      # 上面提到了

## copy
a_copy1 = a[[1,4,6], [2,4,6]]   # 用 index 选
a_copy2 = a[[True, True], [False, True]]  # 用 mask
a_copy3 = a[[1,2], :]        # 虽然 1,2 的确连在一起了, 但是他们确实是 copy
a_copy4 = a[a[1,:] != 0, :]  # fancy indexing
a_copy5 = a[np.isnan(a), :]  # fancy indexing

## 1.使用 np.take(), 替代用 index 选数据的方法.
a = np.random.rand(1000000, 10) #  Uniformly distributed values.
N = 99
indices = np.random.randint(0, 1000000, size=10000)

def f1(a):
    for _ in range(N):
        _ = np.take(a, indices, axis=0)

def f2(b):
    for _ in range(N):
        _ = b[indices]

print('%f' % ((t1-t0)/N))    # 0.000393
print('%f' % ((t2-t1)/N))    # 0.000569

## 2.使用 np.compress(), 替代用 mask 选数据的方法.
mask = a[:, 0] < 0.5
def f1(a):
    for _ in range(N):
        _ = np.compress(mask, a, axis=0)

def f2(b):
    for _ in range(N):
        _ = b[mask]

print('%f' % ((t1-t0)/N))    # 0.028109
print('%f' % ((t2-t1)/N))    # 0.031013

### 用out参数
a = a + 1         # 0.035230
a = np.add(a, 1)  # 0.032738， 可能是 a=a+1 要先转换成 np.add() 这种形式再运算, 所以前者要用更久一点的时间.
# 我们就会触发之前提到的 copy 原则，但是在功能里面有一个 out 参数, 让我们不必要重新创建一个 a. 
a += 1                 # 0.011219
np.add(a, 1, out=a)    # 0.008843


## 给数据命名
a = np.zeros(3, dtype=[('foo', np.int32), ('bar', np.float16)])
b = pd.DataFrame(np.zeros((3, 2), dtype=np.int32), columns=['foo', 'bar'])
b['bar'] = b['bar'].astype(np.float16)

"""
# a
array([(0,  0.), (0,  0.), (0,  0.)],
      dtype=[('foo', '<i4'), ('bar', '<f2')])

# b
   foo  bar
0    0  0.0
1    0  0.0
2    0  0.0
"""

def f1(a):
    for _ in range(N):
        a['bar'] *= a['foo']

def f2(b):
    for _ in range(N):
        b['bar'] *= b['foo']

print('%f' % ((t1-t0)/N))    # 0.000003
print('%f' % ((t2-t1)/N))    # 0.000508



































