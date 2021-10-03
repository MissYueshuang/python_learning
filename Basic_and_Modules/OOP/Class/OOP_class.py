# -*- coding: utf-8 -*-
"""
Created on Thu Jun 25 17:19:42 2020

@author: rmileng
"""

class Student(object):

    def __init__(self, name, score):
        self.name = name
        self.score = score

    def print_score(self):
        print('%s: %s' % (self.name, self.score))
        
bart = Student('Bart Simpson', 59)
lisa = Student('Lisa Simpson', 87)
bart.print_score()
lisa.print_score()

class Student(object):
    def __init__(self, name, gender):
        self.___name = name
        self.__gender = gender
        
    def get_gender(self):
        return self.__gender
    
    def set_gender(self, gender):
        self.__gender = gender
        
bart = Student('Bart', 'male')
if bart.get_gender() != 'male':
    print('测试失败!')
else:
    bart.set_gender('female')
    if bart.get_gender() != 'female':
        print('测试失败!')
    else:
        print('测试成功!')

# 为了统计学生人数，可以给Student类增加一个类属性，每创建一个实例，该属性自动增加：        
class Student(object):
    count = 0
    
    def __init__(self, name):
        self.name = name
        Student.count += 1
    
if Student.count != 0:
    print('测试失败!')
else:
    bart = Student('Bart')
    if Student.count != 1:
        print('测试失败!')
    else:
        lisa = Student('Bart')
        if Student.count != 2:
            print('测试失败!')
        else:
            print('Students:', Student.count)
            print('测试通过!')  

# 请利用@property给一个Screen对象加上width和height属性，以及一个只读属性resolution
class Screen(object):
    @property
    def width(self):
        return self._width
    
    @width.setter
    def width(self,value1):
        self._width = value1

    @property
    def height(self):
        return self._height
    
    @height.setter
    def height(self,value2):
        self._height = value2
        
    @property
    def resolution(self):
        return self._height*self._width
# 测试:
s = Screen()
s.width = 1024
s.height = 768
print('resolution =', s.resolution)
if s.resolution == 786432:
    print('测试通过!')
else:
    print('测试失败!')

# 定制类    
class Student(object):
     def __init__(self, name):
         self.name = name
     def __str__(self):
         return 'Student object (name: %s)' % self.name

print(Student('Michael'))

#
class Fib(object): ## something wrong
    def __getitem__(self, n):
        if isinstance(n, int): # n是索引
            a, b = 1, 1
            for x in range(n):
                a, b = b, a + b
            return a
        if isinstance(n, slice): # n是切片
            start = n.start
            end = n.stop
            if start is None:
                start = 0
            a, b = 1, 1
            f = []
            for x in range(end):                
                if x >= start:
                    f.append(a)
                a, b = b, a + b                
            return f

class Fibo(object):
    def __init__(self):
        self.a, self.b = 0, 1 # 初始化两个计数器a，b

    def __iter__(self):
        return self # 实例本身就是迭代对象，故返回自己

    def __next__(self):
        self.a, self.b = self.b, self.a + self.b # 计算下一个值
        if self.a > 100000: # 退出循环的条件
            raise StopIteration()
        return self.a # 返回下一个值
    





