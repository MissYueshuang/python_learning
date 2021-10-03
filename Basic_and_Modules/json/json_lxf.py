# -*- coding: utf-8 -*-
"""
Created on Tue Jul  7 12:42:57 2020

@author: rmileng
"""
import json

jsonStr = '{"name":"aspiring", "age": 17, "hobby": ["money","power", "read"],"parames":{"a":1,"b":2}}'
 
# 将json格式的字符串转为python数据类型的对象
jsonData = json.loads(jsonStr)
print(jsonData)
print(type(jsonData))
print(jsonData['hobby'])
 
# 加载json文件
path1 = r'D:\LYS\python_learning\Liaoxuefeng_learning\jjj.json'
 
with open(path1,'rb') as f:
    data = json.load(f)
    print(data)
    # 字典类型
    print(type(data))

# class to json
class Student(object):
    def __init__(self, name, age, score):
        self.name = name
        self.age = age
        self.score = score

def student2dict(std):
    return {
        'name': std.name,
        'age': std.age,
        'score': std.score
    }
    
s = Student('Bob', 20, 88)
print(json.dumps(s,default=student2dict))
print(json.dumps(s,default= lambda obj: obj.__dict__))

def dict2student(d):
    return Student(d['name'], d['age'], d['score'])

json_str = '{"age": 20, "score": 88, "name": "Bob"}'
print(json.loads(json_str,object_hook=dict2student))