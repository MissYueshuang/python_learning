# -*- coding: utf-8 -*-
"""
Created on Sun May 31 12:12:33 2020

@author: rmileng
"""
import zipfile
import os

startdir = r'D:\LYS\python_learning\pydata-book-2nd-edition'  #要压缩的文件夹路径
file_news = startdir +'.zip' # 压缩后文件夹的名字
z = zipfile.ZipFile(file_news,'w',zipfile.ZIP_DEFLATED) #参数一：文件夹名
for dirpath, dirnames, filenames in os.walk(startdir):
    fpath = dirpath.replace(startdir,'') #这一句很重要，不replace的话，就从根目录开始复制
    fpath = fpath and fpath + os.sep or ''#这句话理解我也点郁闷，实现当前文件夹以及包含的所有文件的压缩
    for filename in filenames:
        z.write(os.path.join(dirpath, filename),fpath+filename)
#        print ('压缩成功')
z.close()

# extract
z = zipfile.ZipFile(file_news,'r')
for file in z.namelist():
    z.extract(file, 'D:\LYS\temp files') # extract file to your path d:/Work
z.close()
z.extractall(r'D:\LYS\temp files') # the same as the loop

