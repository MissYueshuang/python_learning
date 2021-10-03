# -*- coding: utf-8 -*-
"""
Created on Wed Feb  5 14:31:37 2020

@author: rmileng
"""
## python 控制浏览器
from selenium import webdriver

#import sys
#sys.path
#sys.path.append(r'C:\Users\rmileng\AppData\Local\Google\Chrome\Application')

driver = webdriver.Chrome(r'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
driver.get("https://morvanzhou.github.io/tutorials/data-manipulation/scraping/5-01-selenium/")
driver.find_element_by_link_text(u"赞助").click()
driver.find_element_by_link_text("About").click()
driver.find_element_by_link_text(u"教程 ▾").click()
driver.find_element_by_xpath("//nav[@id='home-nav']/ul/li[6]/ul/li").click()
driver.find_element_by_link_text(u"推荐学习顺序").click()

html = driver.page_source       # get html
driver.get_screenshot_as_file(r"D:\LYS\python learning\result_files\img\sreenshot1.png")
driver.close()
print(html[:200])


from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument("--headless")       # define headless

# add the option when creating driver
driver = webdriver.Chrome(chrome_options=chrome_options)    
driver.get("https://morvanzhou.github.io/")
driver.find_element_by_xpath(u"//img[@alt='强化学习 (Reinforcement Learning)']").click()
driver.find_element_by_link_text("About").click()
driver.find_element_by_link_text(u"赞助").click()
driver.find_element_by_link_text(u"教程 ▾").click()
driver.find_element_by_link_text(u"数据处理 ▾").click()
driver.find_element_by_link_text(u"网页爬虫").click()

html = driver.page_source           # get html
driver.get_screenshot_as_file("./img/sreenshot2.png")
driver.close()
print(html[:200])


'''
important functions:
    web = webdriver.Chrome() # 打开chrome
    web.get(url) # 打开url网页
    web.save_screen_shot(path) #截图
    web.page_source # 获取当前浏览器的当前页的源码（html） 
    bro.execute_script('window.scrollTo(0,document.body.scrollHeight)')  # 执行js代码（让滚动条向下偏移n个像素),下拉到页面底部
    bro.execute_script('window.scrollTo(document.body.scrollHeight,0)')  # 执行js代码（让滚动条向下偏移n个像素),上拉到页面顶部
    js = 'var q=document.documentElement.scrollTop=1000000'
    driver.execute_script(js)
    web.quit() # 关闭chrome
'''
'''
 #设置chrome浏览器无界面模式
    from selenium.webdriver.chrome.options import Options
    chrome_options=Options()
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(r'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe',chrome_options=chrome_options)
'''

