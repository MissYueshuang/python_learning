# -*- coding: utf-8 -*-
"""
Created on Tue Mar 16 15:24:16 2021

@author: ys.leng
"""
import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
dblist = myclient.list_database_names()

# create a new db
mydb = myclient["runoobdb"] #new db
mycol = mydb["sites"] # new collection
mydict = { "name": "RUNOOB", "alexa": "10000", "url": "https://www.runoob.com" }
myclient.list_database_names()
x = mycol.insert_one(mydict) # only after insert a record will the db be created
myclient.list_database_names()
print(x)

# insert
mydict = { "name": "Google", "alexa": "1", "url": "https://www.google.com" }
x = mycol.insert_one(mydict)
print(x.inserted_id)

mylist = [
  { "name": "Taobao", "alexa": "100", "url": "https://www.taobao.com" },
  { "name": "QQ", "alexa": "101", "url": "https://www.qq.com" },
  { "name": "Facebook", "alexa": "10", "url": "https://www.facebook.com" },
  { "name": "知乎", "alexa": "103", "url": "https://www.zhihu.com" },
  { "name": "Github", "alexa": "109", "url": "https://www.github.com" }
]
 
x = mycol.insert_many(mylist)
print(x.inserted_ids)

# find
x = mycol.find_one()
print(x)

for x in mycol.find({ "name": "RUNOOB" }):
  print(x)
  
for x in mycol.find({ "name": { "$gt": "H" } }):
  print(x)
  
for x in mycol.find({ "name": { "$regex": "^R" }}):
  print(x)
  
myresult = mycol.find().limit(3)
 

# modify
myquery = { "alexa": "10000" }
newvalues = { "$set": { "alexa": "12345" } }
mycol.update_one(myquery, newvalues)
mycol.find({"alexa": "12345"})[0]

myquery = { "name": { "$regex": "^F" } }
newvalues = { "$set": { "alexa": "123" } }
x = mycol.update_many(myquery, newvalues)
print(x.modified_count, "文档已修改")

myquery = { "name": {"$regex": "^F"} }
x = mycol.delete_many(myquery)
mycol.find({ "name": {"$regex": "^F"} })[0]
