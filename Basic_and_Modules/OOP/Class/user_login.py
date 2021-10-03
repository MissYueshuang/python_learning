# -*- coding: utf-8 -*-
"""
Created on Wed Jul 22 17:10:15 2020

在该类中实现登录、退出方法, 登录成功将状态(status)修改为True, 
退出将状态修改为False(退出要判断是否处于登录状态).
密码输入错误三次将设置锁定时间(下次登录如果和当前时间比较大于10秒即不允许登录).

@author: rmileng
"""

import json
import time
import pathlib
import os
import sys

# base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#print(base_dir)
base_dir = 'D:\LYS\python_learning\exercise'
sys.path.append('D:\LYS\python_learning\exercise')

class User:
    def __init__(self):
        while True:
            self.name = input('please input username\n>>>:')
            if not self.file_exist(base_dir):
                print('wrong password')
            else:
                break
            self.data = self.db
   
    # 通过判断指定路径下，以用户名命名的文件是否存在，来判断用户输入的用户正确        
    def file_exist(self,path):
        global file_path
        file_name = 'db %s.json' % self.name
        file_path = os.path.join(path,file_name)
        file_is = pathlib.Path(file_path)
        file_result = file_is.is_file()
        if file_result:
            return file_path
        else:
            return False

    @property
    def db(self):
        with open(file_path,'r',encoding='utf-8') as file:
            data = json.load(file)
            return data
    
    def login(self):
        count = 0
        while count < 3:
            if self.data['timeout'] != 0:
                if time.time() - self.db['timeout'] > 10:
                    print('run out of time!')
                    return False
            with open(file_path,'r+',encoding='utf-8') as f:
                count += 1
                password = input('please input your password\n>>>:')
                if password != self.db['password']:
                    print('password is not correct!')
                    if count == 3:
                        self.data['timeout'] = time.time()
                        f.seek(0)
                        f.truncate()
                        json.dump(self.data,f)
                    continue
                
                self.data['status'] = True
                f.seek(0)
                f.truncate()
                json.dump(self.data,f)
                print('----welcome----')
                return True
    
    def exit(self):
        with open(file_path,'r+',encoding = 'utf-8') as f:
            data = json.load(f)
            if data['status']:
                data['status'] = False
                f.seek(0)
                f.truncate()
                json.dump(data,f)
            else:
                print('you already logged out')
  

user1 = User()

user1.login()
print(user1.__dict__)
user1.exit()              
                
                
                
                
                