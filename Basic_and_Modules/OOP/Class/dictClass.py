# -*- coding: utf-8 -*-
"""
Created on Wed Jul 22 16:25:06 2020

@author: rmileng
"""

# exersice 1
class Student():
    def __init__(self,name,age,score):
        self.name = name
        self.age = age
        self.score = score
        
    def get_name(self):
        if isinstance(self.name,str):
            return self.name
    
    def get_age(self):
        if isinstance(self.age,int):
            return self.age
        else:
            return int(self.age)
        
    def get_course(self):
        return max(self.score)
    
zm = Student('zhangming',20,[69,88,100])   
print(zm.get_name())
print(zm.get_age())
print(zm.get_course())

# exersice 2
class Dictclass():
    def __init__(self,class1):
        self.classs = class1
        
    def del_dict(self,key):
        if key in self.classs:
            self.classs.pop(key)
            return self.classs
        return "no need to delete"
    
    def get_dict(self,key):
        if key in self.classs:
            return self.classs[key]
        else:
            print("not found")
        #   return "not found"
            
    def get_key(self):
        return [li for li in self.classs] 

    def update_dict(self,class2):
        # 方法1
        # self.classs.update(dict1)
        # 方法2,对于重复的key，B会覆盖A
        a = dict(self.classs, **class2)
        return a

a = Dictclass({"姓名": "张三", "年龄": "18", "性别": "男"})
print(a.del_dict("年龄"))
print(a.get_dict("姓名"))
print(a.get_key())
print(a.update_dict({"年薪": 0}))