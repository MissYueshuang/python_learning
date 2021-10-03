# -*- coding: utf-8 -*-
"""
Created on Fri Jul 10 16:39:19 2020

@author: rmileng
"""

import sqlite3

conn = sqlite3.connect(r'D:\LYS\python_learning\Liaoxuefeng_learning\test.db')
cursor = conn.cursor()
cursor.execute('create table user (id varchar(20) primary key, name varchar(20))')
# cursor.execute('create table catalog (id integer primary key,pid integer,name varchar(10) UNIQUE）') 上面语句创建了一个叫catalog的表，它有一个主键id，一个pid，和一个name，name是不可以重复的。
cursor.execute(r'insert into user values (1, "lys")')
cursor.execute(r'insert into user values (2, "zyx")')
cursor.execute(r'insert into user values (3, "xk")')
# 如果SQL语句带有参数，那么需要把参数按照位置传递给execute()方法，有几个?占位符就必须对应几个参数 
# cursor.execute('select * from user where name=? and pwd=?', ('abc', 'password'))
cursor.close()
conn.commit()
cursor.close()


conn = sqlite3.connect(r'D:\LYS\python_learning\Liaoxuefeng_learning\test.db')
cursor = conn.cursor()
cursor.execute('select * from user')
values = cursor.fetchall() # 结果集是一个list，每个元素都是一个tuple，对应一行记录。
values = cursor.fetchone()
# cursor.rowcount
cursor.close()
conn.close()


# testing
import os, sqlite3

db_file = r'D:\LYS\python_learning\Liaoxuefeng_learning\practice.db'
if os.path.isfile(db_file):
    os.remove(db_file)

# 初始数据:
conn = sqlite3.connect(db_file)
cursor = conn.cursor()
cursor.execute('create table user(id varchar(20) primary key, name varchar(20), score int)')
cursor.execute(r"insert into user values ('A-001', 'Adam', 95)")
cursor.execute(r"insert into user values ('A-002', 'Bart', 62)")
cursor.execute(r"insert into user values ('A-003', 'Lisa', 78)")
cursor.close()
conn.commit()
conn.close()

def get_score_in(low, high):
    ' 返回指定分数区间的名字，按分数从低到高排序 '
    conn = sqlite3.connect(r'D:\LYS\python_learning\Liaoxuefeng_learning\practice.db')
    cursor = conn.cursor()
    cursor.execute("select name from user where score between ? and ? order by score",(low,high))
    values = cursor.fetchall()
    return [value[0] for value in values]
    
# 测试:
assert get_score_in(80, 95) == ['Adam'], get_score_in(80, 95)
assert get_score_in(60, 80) == ['Bart', 'Lisa'], get_score_in(60, 80)
assert get_score_in(60, 100) == ['Bart', 'Lisa', 'Adam'], get_score_in(60, 100)

print('Pass')