# -*- coding: utf-8 -*-
"""
Created on Tue Jul 21 15:51:36 2020

https://www.cnblogs.com/huang-yc/p/9012822.html

@author: rmileng
"""
# myclass
class exc():
    def __init__(self,host,port,db,charset):
        self.conn = host
        self.port = port
        self.db = db
        self.charset = charset

    def exc1(self,sql):
        conn = connect(self.conn,self.host,self.port,self.db,self.charset)
        conn.execute(sql)
        return xxx
    
    def exc2(self,proc_name):
        conn = connect(self.conn,self.host,self.port,self.db,self.charset)
        conn.call_proc(sql)
        return xxx

test = exc('127.0.0.1',3306,'db1','utf8')
test.exc1('select * from tb1;')
test.exc2('存储过程的名字')

# answer
class Exc:
    host = '127.0.0.1'
    port = 3306
    db = 'db1'
    charset = 'utf8'
    conn = connect(host, port, db, charset)

    def __init__(self, proc_name):
        self.proc = proc_name

    def test(self):
        if self.proc =='select * from tb1;':
            self.conn.execute(sql)
        elif self.proc =='存储过程的名字':
            self.conn.call_proc(sql)
        return XXX

exc1 = Exc('select * from tb1;')
exc1.test()
exc2 = Exc('存储过程的名字')
exc2.test()

# 私有属性
class People(object):
      __name = "luffy"
      __age = 18

p1 = People()
print(p1._People__name, p1._People__age) # 不能直接访问

# __new__
class People(object):
    
    def __init__(self):
       print("__init__")
    
    def __new__(cls, *args, **kwargs):
       print("__new__")
       return object.__new__(cls, *args, **kwargs)

People()

# staticmethod and class method   
class A(object):

   def foo(self, x):
       print("executing foo(%s, %s)" % (self,x))

   @classmethod
   def class_foo(cls, x):
       print("executing class_foo(%s, %s)" % (cls,x))

   @staticmethod
   def static_foo(x):
       print("executing static_foo(%s)" % (x))

a = A()    

#classmehtod是给类用的，即绑定到类，类在使用时会将类本身当做参数传给类方法的第一个参数（即便是对象来调用也会将类当作第一个参数传入

#classmethod，绑定到类的方法
a.class_foo('绑定到类')  #输出结果：executing class_foo(<class '__main__.A'>, 绑定到类)
A.class_foo('绑定到类')  #输出结果：executing class_foo(<class '__main__.A'>, 绑定到类)

#在类内部用staticmethod装饰的函数即非绑定方法，就是普通函数,statimethod不与类或对象绑定，谁都可以调用，没有自动传值效果

#staticmethod 静态方法
a.static_foo('静态绑定')  #输出结果：executing static_foo(静态绑定)
A.static_foo('静态绑定')  #输出结果：executing static_foo(静态绑定)

# @property使eat的接口发生了改变
class Dog(object):

   def __init__(self,name):
       self.name = name

   @property
   def eat(self):
       print(" %s is eating" %self.name)

d = Dog("ChenRonghua")
d.eat # d.eat() will report error

# 继承和封装
class Parent(object):
   x = 1

class Child1(Parent):
   pass

class Child2(Parent):
   pass

print(Parent.x, Child1.x, Child2.x)
Child1.x = 2
print(Parent.x, Child1.x, Child2.x)
Parent.x = 3
print(Parent.x, Child1.x, Child2.x)

# 1 1 1 继承自父类的类属性x，所以都一样，指向同一块内存地址
# 1 2 1 更改Child1，Child1的x指向了新的内存地址
# 3 2 3 更改Parent，Parent的x指向了新的内存地址


# 多态
class Cat(Animal): #属于动物的另外一种形态：猫
     def talk(self):
         print('say miao')
 
def func(animal): #对于使用者来说，自己的代码根本无需改动
     animal.talk()
     
cat1=Cat() #实例出一只猫
func(cat1) #甚至连调用方式也无需改变，就能调用猫的talk功能
#say miao

# 编写程序, 编写一个学生类, 要求有一个计数器的属性, 统计总共实例化了多少个学生.
class student():
    count = 0
    
    @classmethod
    def __init__(cls):
        cls.count += 1

a1 = student()
a2 = student()
student.count

# A 继承了 B, 俩个类都实现了 handle 方法, 在 A 中的 handle 方法中调用 B 的 handle 方法
class B:
    def handle(self):
        print('from B')

class A(B):
    def handle(self):
        super().handle()

a = A()
a.handle()

# 
import json
eg={
    "egon":{"password":"123",'status':False,'timeout':0},
    "alex":{"password":"456",'status':False,'timeout':0},
}
with open('uesr_data.json', 'w', encoding='utf-8') as fp1:
    json.dump(eg,fp1)

class User:
    @property
    def db(self):
        with open('uesr_data.json', 'r', encoding='utf-8') as fp:
            data = json.load(fp)
            return data

obj = User()        
print(obj.db)



