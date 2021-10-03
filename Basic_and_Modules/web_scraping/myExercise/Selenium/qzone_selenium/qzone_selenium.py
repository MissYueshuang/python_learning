# -*- coding: utf-8 -*-
"""
Created on Thu Feb 13 15:46:05 2020

@author: rmileng
"""
from bs4 import BeautifulSoup
from selenium import webdriver
from lxml import etree
import time


driver = webdriver.Chrome(r'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
driver.get('https://qzone.qq.com/')
driver.switch_to_frame('login_frame')
driver.find_element_by_id("switcher_plogin").click()

#driver.find_element_by_id("u").click()
#driver.find_element_by_id("u").clear()
driver.find_element_by_id("u").send_keys("412781823")
#driver.find_element_by_id("p").click()
#driver.find_element_by_id("p").clear()
driver.find_element_by_id("p").send_keys("7993725SHUANG")

driver.find_element_by_id("login_button").click()
time.sleep(2)
driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')
time.sleep(2)
driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')
time.sleep(2)
driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')
time.sleep(2)
page_text = driver.page_source

## method one
tree = etree.HTML(page_text)
li_list = tree.xpath('//ul[@id="feed_friend_list"]/li')
for li in li_list:
    text_list = li.xpath('.//div[@class="f-info"]//text()|.//div[@class="f-info qz_info_cut"]//text()')
    text = ''.join(text_list)
    print(text+'\n\n\n')
driver.close()

## method two (write on your own)
soup = BeautifulSoup(page_text,'lxml')
text = soup.find_all('div',{'class':'f-info'})
all_comments = [l.get_text().strip() for l in text]
all_comments = [l for l in all_comments if l!='']


