# -*- coding: utf-8 -*-
"""
Created on Thu Feb 13 14:43:06 2020

@author: rmileng
"""
from selenium import webdriver
from time import sleep
import time


if __name__ == '__main__':
    url = 'https://movie.douban.com/typerank?type_name=%E6%81%90%E6%80%96&type=20&interval_id=100:90&action='
    # 发起请求前，可以让url表示的页面动态加载出更多的数据
    path = r'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe'
    # 创建无界面的浏览器对象
    bro = webdriver.Chrome(path)
    # 发起url请求
    bro.get(url)
    time.sleep(3)
    # 截图
    bro.save_screenshot(r'D:\LYS\python learning\web_scraping\myexercise\douban_movie250\selenium\1.png')
    # 执行js代码（让滚动条向下偏移n个像素（作用：动态加载了更多的电影信息））
    js = 'window.scrollTo(0,document.body.scrollHeight)'
    bro.execute_script(js)  # 该函数可以执行一组字符串形式的js代码
    time.sleep(2)
    bro.execute_script(js)  # 该函数可以执行一组字符串形式的js代码
    time.sleep(2)
    bro.save_screenshot(r'D:\LYS\python learning\web_scraping\myexercise\douban_movie250\selenium\2.png') 
    time.sleep(2) 
    # 使用爬虫程序爬去当前url中的内容 
    html_source = bro.page_source # 该属性可以获取当前浏览器的当前页的源码（html） 
    with open(r'D:\LYS\python learning\web_scraping\myexercise\douban_movie250\source.html', 'w', encoding='utf-8') as fp: 
        fp.write(html_source) 
    bro.quit()

'''
important functions:
    web = webdriver.Chrome() # 打开chrome
    web.get(url) # 打开url网页
    web.save_screen_shot(path) #截图
    web.page_source # 获取当前浏览器的当前页的源码（html） 
    bro.execute_script('window.scrollTo(0,document.body.scrollHeight)')  # 执行js代码（让滚动条向下偏移n个像素),下拉到页面底部
    bro.execute_script('window.scrollTo(document.body.scrollHeight,0)')  # 执行js代码（让滚动条向下偏移n个像素),上拉到页面顶部
    web.quit() # 关闭chrome
'''