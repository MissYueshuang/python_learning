# -*- coding: utf-8 -*-
"""
Created on Sun Nov 29 15:22:29 2020

@author: rmileng
"""

import numpy as np

print(np.__version__)
np.show_config()

#  test whether none of the elements of a given array is zero.
A = np.array([2,3,7,0])
np.any(A)

# test a given array element-wise for finiteness (not infinity or not a Number).
A = np.array([2,3,7,0,np.nan,np.inf])
np.isfinite(A)

# test element-wise for positive or negative infinity. 
A = np.array([2,7,0,np.nan,np.inf,-np.inf])
np.isfinite(A)
np.sign(A)
np.isinf(A)
np.isnan(A)

# test element-wise for complex number, real number of a given array. Also test whether a given number is a scalar type or not.
a = np.array([1+1j, 1+0j, 4.5, 3, 2, 2j])
np.iscomplex(a)
np.isreal(a)
np.isscalar([3.1])

# two arrays are element-wise equal within a tolerance.
a = np.array([1,2,3])
b = np.array([1,2,3.01])
np.allclose(a,b,0.001)

# create an element-wise comparison (greater, greater_equal, less and less_equal) of two given arrays.
a = np.array([1,2,3])
b = np.array([1,0,4])
np.greater(a,b)

# 12 size of the memory occupied by the array.
a.size*a.itemsize

# 13 create an array of 10 zeros,10 ones, 10 fives.
a = np.array([0,1,5])
np.repeat(a,10)
np.tile(a,10)
np.ones(10)

# 14  create an array of the integers from 30 to70
np.arange(30,71,step=2)

# 16. create a 3x3 identity matrix.
np.identity(3)

# generate a random number between 0 and 1.
a = np.random.random(10)
for x in np.nditer(a):
  print(x,end=" ")
for i,j in np.nditer([a, b]):
    print(i,j)

# create a vector of length 10 with values evenly distributed between 5 and 50.
np.linspace(5,49,5)

# create a vector with values from 0 to 20 and change the sign of the numbers in the range from 9 to 15.
a = np.arange(0,20)
np.negative(a[9:16])

# create a vector of length 5 filled with arbitrary integers from 0 to 10.
np.random.randint(0,11,5)
np.multiply(a,b)

# create a 10x10 matrix, in which the elements on the borders will be equal to 1, and inside 0.
a = np.ones((10,10))
a[1:-1,1:-1] = 0

# create a 5x5 zero matrix with elements on the main diagonal equal to 1, 2, 3, 4, 5.
a = np.zeros((5,5))
np.diag([1,2,3,4,5])

# create a 4x4 matrix in which 0 and 1 are staggered, with zeros on the main diagonal. 
a = np.zeros((4,4))
a[::2,1::2] = 1
a[1::2,::2] = 1


