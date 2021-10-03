# -*- coding: utf-8 -*-
"""
Created on Tue Feb  4 16:46:01 2020

下载文件

@author: rmileng
"""
IMAGE_URL = r"https://morvanzhou.github.io/static/img/description/my_pic.jpg"

# method1: urlretrieve
from urllib.request import urlretrieve
urlretrieve(IMAGE_URL, r'D:\LYS\python learning\result_files\morvan.jpg') # save it in the second path

# request download
import requests
r = requests.get(IMAGE_URL)
with open(r'D:\LYS\python learning\result_files\image2.jpg', 'wb') as f:
    f.write(r.content)                      # whole document
    
# download chunck by chunck： for big files like mp4 (difficult)
# Set stream = True in get() function. This is more efficient 
r = requests.get(IMAGE_URL, stream=True)    # stream loading. load step by step
with open(r'D:\LYS\python learning\result_files\image3.jpg', 'wb') as f:
    for chunk in r.iter_content(chunk_size=32):
        f.write(chunk)   

##################################################
from bs4 import BeautifulSoup
import requests
import re

URL = "http://www.nationalgeographic.com.cn/animals/"
html = requests.get(URL).text
soup = BeautifulSoup(html,'lxml')
img_ul = soup.find_all('ul',{'class':'img_list'})

for ul in img_ul:
    imgs = ul.find_all('img')
    for img in imgs:
        url = img['src']
        r = requests.get(url,stream=True)
        image_name = url.split('/')[-1]
        with open(r'D:\LYS\python learning\result_files\%s.jpg'%image_name, 'wb') as f:
            for chunk in r.iter_content(chunk_size=128):
                f.write(chunk)
            print('Saved %s'%image_name)