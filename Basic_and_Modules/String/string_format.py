# -*- coding: utf-8 -*-
"""
Created on Sat Aug 15 16:52:41 2020

reference: https://pythonpedia.com/en/tutorial/1019/string-formatting

@author: rmileng
"""
# Note you can refer to the same argument more than once, and in arbitrary order within the string.
'Value 0 = {0:1.3f}, value 1 = {1:1.3f}, value 0 = {0:1.3f}'.format(1./3., 1./6.)

# “g” format specifier is a general format that can be used to indicate a precision
print('{0:1.3g}'.format(1./3.))
print('{0:1.3g}'.format(4./3.))

#  use the “e” or “E” format modifier to specify scientific notation.
import numpy as np
eps = np.finfo(np.double).eps
print(eps)
print('{0}'.format(eps))
print('{0:1.2f}'.format(eps))
print('{0:1.2e}'.format(eps))  #exponential notation
print('{0:1.2E}'.format(eps))  #exponential notation with capital E

print('the fraction {0} corresponds to {0:1.0%}'.format(0.78))

'''
Python 2.x2.6
The format() method can be used to change the alignment of the string. You have to do it with a format expression of the form :[fill_char][align_operator][width] where align_operator is one of:

< forces the field to be left-aligned within width.
> forces the field to be right-aligned within width.
^ forces the field to be centered within width.
= forces the padding to be placed after the sign (numeric types only).
fill_char (if omitted default is whitespace) is the character used for the padding.

you could achieve the same results using the string functions ljust(), rjust(), center(), zfill()
'''

'{:~<9}, World'.format('Hello')
# 'Hello~~~~, World'

'{:~>9}, World'.format('Hello')
# '~~~~Hello, World'

'{:~^9}'.format('Hello')
# '~~Hello~~'

'{:0=6}'.format(-123)
# '-00123'
