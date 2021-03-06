# -*- coding: utf-8 -*-
"""
Created on Tue Jul 14 16:23:53 2020

@author: rmileng
"""

class Stack: 

    """模拟栈"""

    def __init__(self): 
        self.items = [] 

    def isEmpty(self): 
        return len(self.items)==0  

    def push(self, item): 
        self.items.append(item) 

    def pop(self): 
        return self.items.pop()  

    def peek(self): 
        if not self.isEmpty(): 
            return self.items[len(self.items)-1] 

    def size(self): 
        return len(self.items)

s=Stack() 
print(s.isEmpty())
s.push(4) 
s.push('dog') 
print(s.peek()) 
s.push(True) 
print(s.size()) 
print(s.isEmpty()) 
s.push(8.4)
print(s.pop()) 
print(s.pop()) 
print(s.size())