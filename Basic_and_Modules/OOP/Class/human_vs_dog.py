# -*- coding: utf-8 -*-
"""
Created on Wed Jul 22 15:32:25 2020

@author: rmileng
"""

# 人狗大战
class Role(object):
    def __init__(self,name):
        self.name = name

    def attack(self,enemy):
        enemy.life_value -= self.aggresivity
        
class People(Role):
    aggresivity = 10
    life_value = 100
    
    def __init__(self,name):
        super().__init__(name)

class Dogs(Role):
    aggresivity = 15
    life_value = 80
    
    def __init__(self,name):
        super().__init__(name)

p1 = People('Tom')
p2 = People('Jack')


d1 = Dogs('niker')
d2 = Dogs('geeker')
d3 = Dogs('chaox')

print(p1.aggresivity)

print(p1.life_value)
p1.attack(d1)
print(d1.life_value)
