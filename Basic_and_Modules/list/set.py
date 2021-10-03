# -*- coding: utf-8 -*-
"""
Created on Fri Jan 31 17:33:11 2020

set

@author: rmileng
"""

char_list = ['a', 'b', 'c', 'c', 'd', 'd', 'd']

sentence = 'Welcome Back to This Tutorial'

print(set(char_list))
# {'b', 'd', 'a', 'c'}
 
print(type(set(char_list))) # class=set

print(set(sentence))
# {'l', 'm', 'a', 'c', 't', 'r', 's', ' ', 'o', 'W', 'T', 'B', 'i', 'e', 'u', 'h', 'k'}

print(set(char_list+ list(sentence)))
# {'l', 'm', 'a', 'c', 't', 'r', 's', ' ', 'd', 'o', 'W', 'T', 'B', 'i', 'e', 'k', 'h', 'u', 'b'} # 区分大小写

unique_char = set(char_list)
unique_char.add('x')
# unique_char.add(['y', 'z']) this is wrong
print(unique_char)

# {'x', 'b', 'd', 'c', 'a'}


unique_char.remove('x')
print(unique_char)
# {'b', 'd', 'c', 'a'}

unique_char.discard('d')
print(unique_char)
# {'b', 'c', 'a'}

unique_char.clear()
print(unique_char)
# set()

unique_char = set(char_list)
print(unique_char.difference({'a', 'e', 'i'}))
# {'b', 'd', 'c'}

print(unique_char.intersection({'a', 'e', 'i'}))
# {'a'}

## The Set update() method accepts another iterable such as Set, List, String, Dictionary as a parameter and adds the elements of these iterable to the calling set. 
X = set({1, 2, 3})
Y = set({2, 3, 4})
X.update(Y) # X = {1, 2, 3, 4}