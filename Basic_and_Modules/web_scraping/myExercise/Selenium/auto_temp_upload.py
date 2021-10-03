# -*- coding: utf-8 -*-
"""
Created on Thu Feb 13 18:12:34 2020

@author: rmileng
"""
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from datetime import datetime
import numpy as np
import sys
sys.path.append(r'D:\LYS\python_learning\CRI')
from auto_send_email_onlytext import sent_email_from_outlook

#设置chrome浏览器无界面模式
chrome_options=Options()
chrome_options.add_argument('--headless')
driver = webdriver.Chrome(r'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe',chrome_options=chrome_options)
url = 'https://myaces.nus.edu.sg/htd/'
driver.get(url)
driver.find_element_by_id("userNameInput").click()
driver.find_element_by_id("userNameInput").send_keys("nusstf\\rmileng")
#driver.find_element_by_id("content").click()
#driver.find_element_by_id("loginForm").submit()
driver.find_element_by_id("passwordInput").send_keys("7993725Shuang")
driver.find_element_by_id("submitButton").click()

temp = str(round(np.random.uniform(36.0,37.0),1)) # randomly regerate my temp

if datetime.now().hour < 12: ## in the morning
    driver.find_element_by_name("declFrequency").click()
    Select(driver.find_element_by_name("declFrequency")).select_by_visible_text("AM")
    driver.find_element_by_id("temperature").click()
    driver.find_element_by_id("temperature").clear()    
    driver.find_element_by_id("temperature").send_keys(temp)
    driver.find_element_by_xpath("(//input[@name='symptomsFlag'])[1]").click()
    driver.find_element_by_name("Save").click()
elif datetime.now().hour > 12:
    driver.find_element_by_name("declFrequency").click()
    Select(driver.find_element_by_name("declFrequency")).select_by_visible_text("PM")
    driver.find_element_by_id("temperature").click()
    driver.find_element_by_id("temperature").clear()    
    driver.find_element_by_id("temperature").send_keys(temp)
    driver.find_element_by_xpath("(//input[@name='symptomsFlag'])[1]").click()
    driver.find_element_by_name("Save").click()
driver.quit() # 关闭chrome

sent_email_from_outlook('auto temp upload','体温已经上传啦~~')

## for GH
chrome_options=Options()
chrome_options.add_argument('--headless')
driver = webdriver.Chrome(r'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe',chrome_options=chrome_options)
url = 'https://myaces.nus.edu.sg/htd/'
driver.get(url)
driver.find_element_by_id("userNameInput").click()
driver.find_element_by_id("userNameInput").send_keys("nusstf\\ephgh")
#driver.find_element_by_id("content").click()
#driver.find_element_by_id("loginForm").submit()
driver.find_element_by_id("passwordInput").send_keys("9602204103528Gh!")
driver.find_element_by_id("submitButton").click()

temp = str(round(np.random.uniform(36.0,37.0),1)) # randomly regerate my temp

if datetime.now().hour < 12: ## in the morning
    driver.find_element_by_name("declFrequency").click()
    Select(driver.find_element_by_name("declFrequency")).select_by_visible_text("AM")
    driver.find_element_by_id("temperature").click()
    driver.find_element_by_id("temperature").clear()    
    driver.find_element_by_id("temperature").send_keys(temp)
    driver.find_element_by_xpath("(//input[@name='symptomsFlag'])[1]").click()
    driver.find_element_by_name("Save").click()
elif datetime.now().hour > 12:
    driver.find_element_by_name("declFrequency").click()
    Select(driver.find_element_by_name("declFrequency")).select_by_visible_text("PM")
    driver.find_element_by_id("temperature").click()
    driver.find_element_by_id("temperature").clear()    
    driver.find_element_by_id("temperature").send_keys(temp)
    driver.find_element_by_xpath("(//input[@name='symptomsFlag'])[1]").click()
    driver.find_element_by_name("Save").click()
driver.quit() # 关闭chrome

sent_email_from_outlook('auto temp upload','肖战哥哥，体温已经帮你上传啦~~',['ephgh@nus.edu.sg'])
